"""Rollback controls panel component."""

import streamlit as st
from frontend.styles import Styles


class RollbackPanel:
    """Renders the deployment rollback controls.

    Shows the deployment stack, current version, and the
    emergency rollback button.
    """

    @staticmethod
    def render(rollback_service, log_service) -> None:
        """Render the rollback panel."""
        st.markdown(
            Styles.section_header("🔙", "Rollback de Despliegues"),
            unsafe_allow_html=True,
        )

        col_actions, col_history = st.columns([1, 1])

        # --- Current Version + Rollback Button ---
        with col_actions:
            current = rollback_service.get_current_version()

            if current:
                card_html = f"""
                <div class="deploy-card deploy-card-current">
                    <div style="display:flex; justify-content:space-between;
                         align-items:center;">
                        <div>
                            <div class="deploy-version">
                                🚀 Versión Actual: {current.version}
                            </div>
                            <div class="deploy-detail">
                                Commit: {current.commit_hash} ·
                                {current.deployed_at.strftime('%Y-%m-%d %H:%M:%S')}
                            </div>
                        </div>
                        {Styles.status_badge('active', 'Activo')}
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                st.markdown("")
                stack_size = rollback_service.get_stack_size()
                st.markdown(
                    Styles.metric_box(stack_size, "Versiones Desplegadas"),
                    unsafe_allow_html=True,
                )

                st.markdown("")
                st.markdown(
                    '<div class="rollback-btn">',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "⚠️ Rollback de Emergencia",
                    use_container_width=True,
                    key="rollback_btn",
                ):
                    result = rollback_service.emergency_rollback()
                    if result["success"]:
                        log_service.warn("Rollback", result["message"])
                        st.success(result["message"])
                    else:
                        log_service.error("Rollback", result["reason"])
                        st.warning(result["reason"])
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info(
                    "No hay despliegues registrados. "
                    "Ejecute el pipeline exitosamente para desplegar."
                )

        # --- Deployment History ---
        with col_history:
            st.markdown("##### 📚 Historial de Versiones")

            history = rollback_service.get_history()
            if history:
                for i, dep in enumerate(history):
                    is_top = i == 0
                    card_class = (
                        "deploy-card deploy-card-current"
                        if is_top else "deploy-card"
                    )
                    position = f"🔝 Cima" if is_top else f"#{i + 1}"
                    status = dep["status"]

                    card_html = f"""
                    <div class="{card_class}">
                        <div style="display:flex; justify-content:space-between;
                             align-items:center;">
                            <div>
                                <span class="deploy-version">
                                    {position} — {dep['version']}
                                </span>
                                <div class="deploy-detail">
                                    Commit: {dep['commit_hash']} ·
                                    {dep['deployed_at']}
                                </div>
                            </div>
                            {Styles.status_badge(status, status.capitalize())}
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.info("La pila de despliegues está vacía.")

            # --- Rolled Back History ---
            rolled_back = rollback_service.get_rolled_back_history()
            if rolled_back:
                st.markdown("##### ♻️ Versiones Revertidas")
                for dep in rolled_back:
                    card_html = f"""
                    <div class="deploy-card">
                        <div style="display:flex; justify-content:space-between;
                             align-items:center;">
                            <div>
                                <span class="deploy-version">
                                    {dep['version']}
                                </span>
                                <div class="deploy-detail">
                                    Commit: {dep['commit_hash']} ·
                                    {dep['deployed_at']}
                                </div>
                            </div>
                            {Styles.status_badge('rolled_back', 'Revertido')}
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
