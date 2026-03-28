"""Pipeline stages visualizer component."""

import streamlit as st
from frontend.styles import Styles


class PipelinePanel:
    """Renders the pipeline stages as a visual horizontal flow.

    Each stage is a node in the singly linked list, displayed
    as a colored box connected by arrows.
    """

    # Status icons
    STATUS_ICONS = {
        "pending": "⏳",
        "running": "🔄",
        "success": "✅",
        "failed": "❌",
        "skipped": "⏭️",
    }

    # Spanish labels
    STATUS_LABELS = {
        "pending": "Pendiente",
        "running": "Ejecutando",
        "success": "Exitoso",
        "failed": "Fallido",
        "skipped": "Omitido",
    }

    @classmethod
    def render(
        cls, pipeline_executor, log_service, rollback_service
    ) -> None:
        """Render the pipeline visualizer and controls."""
        st.markdown(
            Styles.section_header("🔗", "Pipeline de CI/CD"),
            unsafe_allow_html=True,
        )

        # --- Pipeline Flow Visualization ---
        stages = pipeline_executor.get_stages()
        if stages:
            flow_html = '<div class="pipeline-container">'
            for i, stage_dict in enumerate(stages):
                status = stage_dict["status"]
                icon = cls.STATUS_ICONS.get(status, "⏳")
                duration = stage_dict.get("duration", 0)
                duration_text = (
                    f"{duration}s" if duration > 0 else ""
                )

                # Determine arrow class
                arrow_class = "pipeline-arrow"
                if status == "success":
                    arrow_class += " pipeline-arrow-active"

                flow_html += f"""
                <div class="pipeline-stage">
                    <div class="pipeline-stage-box stage-{status}">
                        {icon} {stage_dict['name']}
                    </div>
                    <span class="stage-duration">{duration_text}</span>
                </div>
                """

                if i < len(stages) - 1:
                    next_status = stages[i + 1]["status"]
                    arrow_active = ""
                    if status == "success":
                        arrow_active = " pipeline-arrow-active"
                    flow_html += (
                        f'<span class="pipeline-arrow{arrow_active}">→</span>'
                    )

            flow_html += "</div>"
            st.markdown(flow_html, unsafe_allow_html=True)

        # --- Controls ---
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button(
                "🚀 Ejecutar Pipeline",
                use_container_width=True,
                key="run_pipeline_btn",
            ):
                result = pipeline_executor.run_pipeline()
                if result["success"]:
                    # Auto-deploy on success
                    current = rollback_service.get_current_version()
                    version_num = (
                        1 if not current
                        else int(current.version.split(".")[-1]) + 1
                    )
                    new_version = f"v1.0.{version_num}"
                    rollback_service.push_deployment(new_version)
                    log_service.success(
                        "Despliegue",
                        f"Versión {new_version} desplegada a producción.",
                    )
                st.rerun()

        with col2:
            if st.button(
                "🔄 Reiniciar Pipeline",
                use_container_width=True,
                key="reset_pipeline_btn",
            ):
                pipeline_executor.reset()
                log_service.info("Pipeline", "Pipeline reiniciado.")
                st.rerun()

        with col3:
            last = pipeline_executor.last_result
            label = {
                "idle": "⚪ Sin ejecutar",
                "success": "🟢 Último: Exitoso",
                "failed": "🔴 Último: Fallido",
            }.get(last, "⚪ Sin ejecutar")
            st.markdown(
                f"<div style='text-align:center; padding:8px; "
                f"font-family: JetBrains Mono, monospace; "
                f"font-size:14px; color:#c9d1d9;'>{label}</div>",
                unsafe_allow_html=True,
            )
