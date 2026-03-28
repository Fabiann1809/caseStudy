"""CI/CD Pipeline Simulator — Streamlit entry point.

This is the main application file. Run with:
    streamlit run app.py
"""

import streamlit as st

from backend.data_structures.job_queue import JobQueue
from backend.data_structures.rollback_stack import RollbackStack
from backend.data_structures.stage_linked_list import StageLinkedList
from backend.data_structures.log_list import LogList

from backend.services.agent_manager import AgentManager
from backend.services.job_queue_service import JobQueueService
from backend.services.rollback_service import RollbackService
from backend.services.pipeline_executor import PipelineExecutor
from backend.services.log_service import LogService

from frontend.dashboard import Dashboard


def initialize_session_state() -> None:
    """Initialize all service instances in Streamlit session state.

    This ensures data structures persist across Streamlit reruns.
    """
    if "initialized" not in st.session_state:
        # --- Data Structures ---
        st.session_state.job_queue = JobQueue()
        st.session_state.rollback_stack = RollbackStack()
        st.session_state.stage_list = StageLinkedList.build_default()
        st.session_state.log_list = LogList()

        # --- Services ---
        st.session_state.agent_manager = AgentManager()
        st.session_state.job_queue_service = JobQueueService(
            st.session_state.job_queue
        )
        st.session_state.log_service = LogService(
            st.session_state.log_list
        )
        st.session_state.rollback_service = RollbackService(
            st.session_state.rollback_stack
        )
        st.session_state.pipeline_executor = PipelineExecutor(
            stage_list=st.session_state.stage_list,
            log_service=st.session_state.log_service,
        )

        # Welcome log
        st.session_state.log_service.info(
            "Sistema",
            "Sistema de CI/CD iniciado correctamente.",
        )
        st.session_state.log_service.info(
            "Sistema",
            "4 agentes de ejecución configurados: "
            "Ubuntu, Windows, macOS, Alpine.",
        )
        st.session_state.log_service.info(
            "Sistema",
            "Pipeline de 5 etapas listo: Checkout → "
            "Instalar Dependencias → Linter → Pruebas Unitarias → Despliegue.",
        )

        st.session_state.initialized = True


def main() -> None:
    """Application entry point."""
    st.set_page_config(
        page_title="Pipeline CI/CD — Panel de Control",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    initialize_session_state()

    # --- Sidebar ---
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding:10px 0;">
                <span style="font-size:48px;">⚙️</span>
                <h2 style="margin:8px 0 4px 0; font-size:20px;">
                    CI/CD Pipeline
                </h2>
                <p style="font-size:12px; color:#6e7681;
                   font-family:'JetBrains Mono', monospace;">
                    Simulador v1.0
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("### 📖 Guía Rápida")
        st.markdown(
            """
            1. **Agregar Trabajos** a la cola desde
               el formulario
            2. **Procesar** para asignar trabajos a
               los agentes disponibles
            3. **Ejecutar Pipeline** para correr las
               5 etapas del CI/CD
            4. **Rollback** si una versión falla en
               producción
            """
        )



    # --- Main Dashboard ---
    dashboard = Dashboard(
        agent_manager=st.session_state.agent_manager,
        job_queue_service=st.session_state.job_queue_service,
        pipeline_executor=st.session_state.pipeline_executor,
        log_service=st.session_state.log_service,
        rollback_service=st.session_state.rollback_service,
    )
    dashboard.render()


if __name__ == "__main__":
    main()
