"""Main dashboard layout for the CI/CD Pipeline Simulator."""

import streamlit as st

from frontend.styles import Styles
from frontend.components.agent_panel import AgentPanel
from frontend.components.job_panel import JobPanel
from frontend.components.pipeline_panel import PipelinePanel
from frontend.components.log_panel import LogPanel
from frontend.components.rollback_panel import RollbackPanel


class Dashboard:
    """Orchestrates the main dashboard layout.

    Renders all panels in a structured layout and manages
    the overall page configuration.
    """

    def __init__(
        self,
        agent_manager,
        job_queue_service,
        pipeline_executor,
        log_service,
        rollback_service,
    ) -> None:
        self._agent_manager = agent_manager
        self._job_queue_service = job_queue_service
        self._pipeline_executor = pipeline_executor
        self._log_service = log_service
        self._rollback_service = rollback_service

    def render(self) -> None:
        """Render the full dashboard."""
        # Inject custom CSS
        st.markdown(Styles.get_main_css(), unsafe_allow_html=True)

        # --- Header ---
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:14px;
                 padding: 10px 0 20px 0;">
                <span style="font-size:36px;">⚙️</span>
                <div>
                    <h1 style="margin:0; font-size:28px;
                        background: linear-gradient(90deg, #4fc3f7, #81d4fa);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-family: 'Inter', sans-serif;">
                        Pipeline de CI/CD — Panel de Control
                    </h1>
                    <p style="margin:0; font-size:13px; color:#6e7681;
                       font-family: 'JetBrains Mono', monospace;">
                        Simulador de Integración y Despliegue Continuo
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Top metrics bar ---
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            available = len(self._agent_manager.get_available_agents())
            total = len(self._agent_manager.get_agents())
            st.markdown(
                Styles.metric_box(
                    f"{available}/{total}", "Agentes Disponibles"
                ),
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                Styles.metric_box(
                    self._job_queue_service.get_queue_size(),
                    "Trabajos en Cola"
                ),
                unsafe_allow_html=True,
            )
        with m3:
            result_icon = {
                "idle": "⚪",
                "success": "🟢",
                "failed": "🔴",
            }.get(self._pipeline_executor.last_result, "⚪")
            st.markdown(
                Styles.metric_box(result_icon, "Estado del Pipeline"),
                unsafe_allow_html=True,
            )
        with m4:
            current_ver = self._rollback_service.get_current_version()
            ver_text = current_ver.version if current_ver else "—"
            st.markdown(
                Styles.metric_box(ver_text, "Versión en Producción"),
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # --- Section 1: Agents ---
        AgentPanel.render(self._agent_manager)

        st.markdown("---")

        # --- Section 2: Pipeline ---
        PipelinePanel.render(
            self._pipeline_executor,
            self._log_service,
            self._rollback_service,
        )

        st.markdown("---")

        # --- Section 3: Job Queue ---
        JobPanel.render(
            self._job_queue_service,
            self._agent_manager,
            self._log_service,
        )

        st.markdown("---")

        # --- Section 4: Logs ---
        LogPanel.render(self._log_service)

        st.markdown("---")

        # --- Section 5: Rollback ---
        RollbackPanel.render(
            self._rollback_service,
            self._log_service,
        )
