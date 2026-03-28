"""Agent status panel component."""

import streamlit as st
from frontend.styles import Styles


class AgentPanel:
    """Renders the execution agents status panel.

    Shows a card for each virtual server with its OS, current status,
    and assigned job if busy.
    """

    # OS icons mapping
    OS_ICONS = {
        "Ubuntu": "🐧",
        "Windows": "🪟",
        "macOS": "🍎",
        "Alpine": "🏔️",
    }

    @classmethod
    def render(cls, agent_manager) -> None:
        """Render the agent panel with server cards."""
        st.markdown(
            Styles.section_header("🖥️", "Agentes de Ejecución"),
            unsafe_allow_html=True,
        )

        agents = agent_manager.get_agents()
        cols = st.columns(len(agents))

        for col, agent in zip(cols, agents):
            with col:
                icon = cls.OS_ICONS.get(agent.os_type, "💻")
                status_text = "Libre" if agent.is_available() else "Ocupado"
                status_class = "idle" if agent.is_available() else "busy"

                job_info = ""
                if agent.current_job:
                    job_info = f"""
                    <div class="agent-card-detail">
                        📋 {agent.current_job.name}
                    </div>
                    <div class="agent-card-detail">
                        👤 {agent.current_job.developer}
                    </div>
                    """

                card_html = f"""
                <div class="agent-card">
                    <div class="agent-card-header">
                        <p class="agent-card-title">{icon} {agent.name}</p>
                        {Styles.status_badge(status_class, status_text)}
                    </div>
                    <div class="agent-card-os">SO: {agent.os_type}</div>
                    <div class="agent-card-detail">
                        Trabajos completados: {agent.jobs_completed}
                    </div>
                    {job_info}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
