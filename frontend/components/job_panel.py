"""Job queue panel component."""

import streamlit as st
from frontend.styles import Styles


class JobPanel:
    """Renders the job queue panel.

    Includes a form to submit new jobs, a list of pending jobs,
    and buttons to process jobs.
    """

    @staticmethod
    def render(job_queue_service, agent_manager, log_service) -> None:
        """Render the job queue panel."""
        st.markdown(
            Styles.section_header("📋", "Cola de Trabajos"),
            unsafe_allow_html=True,
        )

        col_form, col_queue = st.columns([1, 1])

        # --- Job Submission Form ---
        with col_form:
            st.markdown("##### 📝 Nuevo Trabajo")
            with st.form("job_form", clear_on_submit=True):
                job_name = st.text_input(
                    "Nombre del trabajo",
                    placeholder="ej. build-frontend",
                )
                developer = st.text_input(
                    "Desarrollador",
                    placeholder="ej. Juan Pérez",
                )
                branch = st.text_input(
                    "Rama",
                    placeholder="ej. feature/login",
                )
                submitted = st.form_submit_button(
                    "➕ Agregar a la Cola",
                    use_container_width=True,
                )

                if submitted:
                    if job_name and developer and branch:
                        job = job_queue_service.submit_job(
                            name=job_name,
                            developer=developer,
                            branch=branch,
                        )
                        log_service.info(
                            "JobQueue",
                            f"Trabajo '{job.name}' agregado a la cola "
                            f"por {developer} (rama: {branch})",
                        )
                        st.success(
                            f"✅ Trabajo '{job_name}' agregado a la cola."
                        )
                        st.rerun()
                    else:
                        st.warning("⚠️ Todos los campos son obligatorios.")

        # --- Pending Queue ---
        with col_queue:
            st.markdown("##### 📥 Trabajos Pendientes")

            queue_size = job_queue_service.get_queue_size()
            st.markdown(
                Styles.metric_box(queue_size, "En cola"),
                unsafe_allow_html=True,
            )

            if queue_size > 0:
                st.markdown("")
                if st.button(
                    "▶️ Procesar Siguiente Trabajo",
                    use_container_width=True,
                    key="process_job_btn",
                ):
                    result = job_queue_service.process_next(agent_manager)
                    if result["success"]:
                        log_service.info("JobQueue", result["message"])
                        st.success(result["message"])
                    else:
                        log_service.warn("JobQueue", result["reason"])
                        st.warning(result["reason"])
                    st.rerun()

                # Show queue items
                pending = job_queue_service.get_pending_jobs()
                for i, job_dict in enumerate(pending):
                    position = i + 1
                    job_html = f"""
                    <div class="job-row">
                        <div>
                            <span class="job-name">#{position} {job_dict['name']}</span>
                            <div class="job-detail">
                                👤 {job_dict['developer']} · 🌿 {job_dict['branch']}
                            </div>
                        </div>
                        <div>
                            {Styles.status_badge('queued', 'En Cola')}
                            <div class="job-detail">{job_dict['created_at']}</div>
                        </div>
                    </div>
                    """
                    st.markdown(job_html, unsafe_allow_html=True)
            else:
                st.info("La cola de trabajos está vacía.")

        # --- Complete Jobs on Busy Agents ---
        busy = agent_manager.get_busy_agents()
        if busy:
            st.markdown("##### 🔧 Trabajos en Ejecución")
            for index, agent in busy:
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    job = agent.current_job
                    st.markdown(
                        f"**{agent.name}** ({agent.os_type}) → "
                        f"`{job.name}` por *{job.developer}*"
                    )
                with col_b:
                    if st.button(
                        "✅ Éxito",
                        key=f"success_{index}",
                    ):
                        result = job_queue_service.complete_job(
                            agent_manager, index, success=True
                        )
                        log_service.success("JobQueue", result["message"])
                        st.rerun()
                with col_c:
                    if st.button(
                        "❌ Fallo",
                        key=f"fail_{index}",
                    ):
                        result = job_queue_service.complete_job(
                            agent_manager, index, success=False
                        )
                        log_service.error("JobQueue", result["message"])
                        st.rerun()
