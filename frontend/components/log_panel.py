"""Real-time log viewer component."""

import streamlit as st
from frontend.styles import Styles


class LogPanel:
    """Renders the real-time log console with filtering and search.

    Displays log entries in a console-style viewer with color-coded
    levels and supports filtering by level and keyword search.
    """

    # CSS class for each log level
    LEVEL_CLASSES = {
        "INFO": "log-info",
        "WARN": "log-warn",
        "ERROR": "log-error",
        "SUCCESS": "log-success",
        "DEBUG": "log-debug",
    }

    @classmethod
    def render(cls, log_service) -> None:
        """Render the log console panel."""
        st.markdown(
            Styles.section_header("📜", "Visor de Logs en Tiempo Real"),
            unsafe_allow_html=True,
        )

        # --- Filters ---
        col_filter, col_search, col_count, col_clear = st.columns([1, 2, 1, 1])

        with col_filter:
            level_filter = st.selectbox(
                "Filtrar por nivel",
                options=["TODOS", "INFO", "WARN", "ERROR", "SUCCESS", "DEBUG"],
                key="log_level_filter",
            )

        with col_search:
            search_term = st.text_input(
                "Buscar en logs",
                placeholder="Buscar por palabra clave...",
                key="log_search",
            )

        with col_count:
            total = log_service.get_log_count()
            st.markdown(
                Styles.metric_box(total, "Total de Logs"),
                unsafe_allow_html=True,
            )

        with col_clear:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(
                "🗑️ Limpiar Logs",
                use_container_width=True,
                key="clear_logs_btn",
            ):
                log_service.clear_logs()
                st.rerun()

        # --- Get Filtered Logs ---
        if search_term:
            entries = log_service.search_logs(search_term)
        elif level_filter != "TODOS":
            entries = log_service.filter_logs(level_filter)
        else:
            entries = log_service.get_logs()

        # --- Render Console ---
        if entries:
            log_lines = []
            for entry in entries:
                level_class = cls.LEVEL_CLASSES.get(entry.level, "log-info")
                time_str = entry.timestamp.strftime("%H:%M:%S")
                line = (
                    f'<div class="log-line">'
                    f'<span class="log-timestamp">[{time_str}]</span> '
                    f'<span class="{level_class}">[{entry.level:<7}]</span> '
                    f'<span class="log-stage">[{entry.stage}]</span> '
                    f'<span class="{level_class}">{entry.message}</span>'
                    f"</div>"
                )
                log_lines.append(line)

            console_html = (
                '<div class="log-console">'
                + "\n".join(log_lines)
                + "</div>"
            )
            st.markdown(console_html, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="log-console">'
                '<div class="log-line log-info">'
                "No hay logs para mostrar. Ejecute el pipeline o "
                "agregue trabajos para generar logs."
                "</div></div>",
                unsafe_allow_html=True,
            )
