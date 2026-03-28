"""Pipeline executor — traverses the stage linked list and runs each stage."""

from backend.data_structures.stage_linked_list import StageLinkedList
from backend.services.log_service import LogService


class PipelineExecutor:
    """Executes the CI/CD pipeline by traversing the singly linked list.

    Each stage is run in order. If a stage fails, execution stops
    immediately (subsequent stages are marked as skipped).
    """

    def __init__(
        self,
        stage_list: StageLinkedList,
        log_service: LogService,
    ) -> None:
        """Initialize with a stage linked list and log service."""
        self._stage_list: StageLinkedList = stage_list
        self._log_service: LogService = log_service
        self._last_result: str = "idle"  # idle | success | failed

    # --- Properties ---

    @property
    def stage_list(self) -> StageLinkedList:
        return self._stage_list

    @property
    def last_result(self) -> str:
        return self._last_result

    # --- Execution ---

    def run_pipeline(self, fail_probability: float = 0.15) -> dict:
        """Execute the full pipeline, stage by stage.

        Traverses the linked list from head to tail. A stage only
        invokes the next stage after it finishes successfully.

        Returns a result dict summarizing the run.
        """
        self._stage_list.reset_all()
        self._log_service.info("Pipeline", "Iniciando ejecución del pipeline...")

        current_node = self._stage_list.get_head()
        stage_results: list[dict] = []
        all_passed = True

        while current_node is not None:
            stage = current_node.stage
            self._log_service.info(
                stage.name,
                f"Ejecutando etapa: {stage.name}..."
            )

            passed = stage.execute(fail_probability=fail_probability)

            if passed:
                self._log_service.success(
                    stage.name,
                    f"Etapa '{stage.name}' completada en "
                    f"{stage.duration_seconds}s."
                )
                stage_results.append(stage.to_dict())
                current_node = current_node.next
            else:
                self._log_service.error(
                    stage.name,
                    f"Etapa '{stage.name}' falló: {stage.output}"
                )
                stage_results.append(stage.to_dict())
                all_passed = False

                # Mark remaining stages as skipped
                remaining = current_node.next
                while remaining is not None:
                    remaining.stage.status = "skipped"
                    self._log_service.warn(
                        remaining.stage.name,
                        f"Etapa '{remaining.stage.name}' omitida "
                        f"por fallo anterior."
                    )
                    stage_results.append(remaining.stage.to_dict())
                    remaining = remaining.next
                break

        self._last_result = "success" if all_passed else "failed"

        if all_passed:
            self._log_service.success(
                "Pipeline",
                "✅ Pipeline completado exitosamente."
            )
        else:
            self._log_service.error(
                "Pipeline",
                "❌ Pipeline fallido. Revise los logs para más detalles."
            )

        return {
            "success": all_passed,
            "stages": stage_results,
            "result": self._last_result,
        }

    def get_stages(self) -> list[dict]:
        """Return the current state of all stages."""
        return self._stage_list.to_list()

    def reset(self) -> None:
        """Reset all stages and the pipeline state."""
        self._stage_list.reset_all()
        self._last_result = "idle"

    def __repr__(self) -> str:
        return (
            f"PipelineExecutor(stages={len(self._stage_list)}, "
            f"last_result='{self._last_result}')"
        )
