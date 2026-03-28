"""Custom CSS styles for the CI/CD Pipeline Simulator.

Jenkins-inspired dark industrial theme with navy blue, steel grays,
and green/red status indicators.
"""


class Styles:
    """Contains all custom CSS for the Streamlit application.

    Inspired by the Jenkins CI dashboard: dark navy backgrounds,
    monospace fonts for logs, and industrial color palette.
    """

    @staticmethod
    def get_main_css() -> str:
        """Return the main CSS stylesheet."""
        return """
        <style>
            /* ===== JENKINS-INSPIRED GLOBAL THEME ===== */
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap');

            .stApp {
                background: linear-gradient(135deg, #1a1f36 0%, #0d1117 50%, #161b22 100%);
                color: #c9d1d9;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0d1117 0%, #161b22 100%) !important;
                border-right: 2px solid #21262d;
            }
            section[data-testid="stSidebar"] .stMarkdown h1,
            section[data-testid="stSidebar"] .stMarkdown h2,
            section[data-testid="stSidebar"] .stMarkdown h3 {
                color: #4fc3f7 !important;
            }

            /* Headers */
            h1, h2, h3, h4 {
                font-family: 'Inter', sans-serif !important;
                color: #e6edf3 !important;
            }

            /* ===== CARD COMPONENT ===== */
            .agent-card {
                background: linear-gradient(145deg, #161b22, #1c2333);
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 16px;
                margin: 8px 0;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }
            .agent-card:hover {
                border-color: #4fc3f7;
                box-shadow: 0 0 15px rgba(79, 195, 247, 0.15);
            }

            .agent-card-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 10px;
            }
            .agent-card-title {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                font-weight: 600;
                color: #e6edf3;
                margin: 0;
            }
            .agent-card-os {
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                color: #8b949e;
            }
            .agent-card-detail {
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                color: #8b949e;
                margin-top: 6px;
            }

            /* ===== STATUS BADGE ===== */
            .status-badge {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 12px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .status-idle {
                background: rgba(46, 160, 67, 0.2);
                color: #3fb950;
                border: 1px solid rgba(46, 160, 67, 0.4);
            }
            .status-busy {
                background: rgba(210, 153, 34, 0.2);
                color: #d29922;
                border: 1px solid rgba(210, 153, 34, 0.4);
            }
            .status-success {
                background: rgba(46, 160, 67, 0.2);
                color: #3fb950;
                border: 1px solid rgba(46, 160, 67, 0.4);
            }
            .status-failed {
                background: rgba(248, 81, 73, 0.2);
                color: #f85149;
                border: 1px solid rgba(248, 81, 73, 0.4);
            }
            .status-running {
                background: rgba(79, 195, 247, 0.2);
                color: #4fc3f7;
                border: 1px solid rgba(79, 195, 247, 0.4);
                animation: pulse 1.5s ease infinite;
            }
            .status-pending {
                background: rgba(139, 148, 158, 0.2);
                color: #8b949e;
                border: 1px solid rgba(139, 148, 158, 0.4);
            }
            .status-skipped {
                background: rgba(139, 148, 158, 0.15);
                color: #6e7681;
                border: 1px solid rgba(139, 148, 158, 0.3);
            }
            .status-queued {
                background: rgba(163, 113, 247, 0.2);
                color: #a371f7;
                border: 1px solid rgba(163, 113, 247, 0.4);
            }
            .status-active {
                background: rgba(46, 160, 67, 0.2);
                color: #3fb950;
                border: 1px solid rgba(46, 160, 67, 0.4);
            }
            .status-rolled_back {
                background: rgba(248, 81, 73, 0.2);
                color: #f85149;
                border: 1px solid rgba(248, 81, 73, 0.4);
            }
            .status-superseded {
                background: rgba(139, 148, 158, 0.15);
                color: #6e7681;
                border: 1px solid rgba(139, 148, 158, 0.3);
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.6; }
            }

            /* ===== PIPELINE FLOW ===== */
            .pipeline-container {
                display: flex;
                align-items: center;
                gap: 0;
                padding: 20px 10px;
                overflow-x: auto;
                background: linear-gradient(145deg, #0d1117, #161b22);
                border: 1px solid #21262d;
                border-radius: 10px;
                margin: 10px 0;
            }
            .pipeline-stage {
                flex-shrink: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
                min-width: 120px;
            }
            .pipeline-stage-box {
                padding: 12px 16px;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
                min-width: 100px;
                border: 2px solid;
                transition: all 0.3s ease;
            }
            .stage-pending {
                background: rgba(139, 148, 158, 0.1);
                border-color: #30363d;
                color: #8b949e;
            }
            .stage-running {
                background: rgba(79, 195, 247, 0.15);
                border-color: #4fc3f7;
                color: #4fc3f7;
                animation: pulse 1.5s ease infinite;
                box-shadow: 0 0 20px rgba(79, 195, 247, 0.2);
            }
            .stage-success {
                background: rgba(46, 160, 67, 0.15);
                border-color: #3fb950;
                color: #3fb950;
            }
            .stage-failed {
                background: rgba(248, 81, 73, 0.15);
                border-color: #f85149;
                color: #f85149;
                box-shadow: 0 0 20px rgba(248, 81, 73, 0.2);
            }
            .stage-skipped {
                background: rgba(139, 148, 158, 0.05);
                border-color: #21262d;
                color: #484f58;
            }
            .pipeline-arrow {
                flex-shrink: 0;
                font-size: 20px;
                color: #30363d;
                margin: 0 4px;
                padding-bottom: 20px;
            }
            .pipeline-arrow-active {
                color: #3fb950;
            }
            .stage-duration {
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                color: #6e7681;
            }

            /* ===== LOG CONSOLE ===== */
            .log-console {
                background: #0d1117;
                border: 1px solid #21262d;
                border-radius: 8px;
                padding: 16px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                line-height: 1.6;
                max-height: 400px;
                overflow-y: auto;
                color: #c9d1d9;
            }
            .log-line {
                padding: 2px 0;
                white-space: pre-wrap;
                word-break: break-all;
            }
            .log-info { color: #79c0ff; }
            .log-warn { color: #d29922; }
            .log-error { color: #f85149; }
            .log-success { color: #3fb950; }
            .log-debug { color: #8b949e; }
            .log-timestamp { color: #6e7681; }
            .log-stage { color: #a371f7; }

            /* ===== JOB TABLE ===== */
            .job-row {
                background: linear-gradient(145deg, #161b22, #1c2333);
                border: 1px solid #21262d;
                border-radius: 6px;
                padding: 10px 14px;
                margin: 6px 0;
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
            }
            .job-name {
                font-weight: 600;
                color: #e6edf3;
            }
            .job-detail {
                color: #8b949e;
                font-size: 11px;
            }

            /* ===== DEPLOYMENT CARD ===== */
            .deploy-card {
                background: linear-gradient(145deg, #161b22, #1c2333);
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 14px;
                margin: 6px 0;
                font-family: 'JetBrains Mono', monospace;
            }
            .deploy-card-current {
                border-color: #3fb950;
                box-shadow: 0 0 10px rgba(46, 160, 67, 0.15);
            }
            .deploy-version {
                font-size: 14px;
                font-weight: 700;
                color: #e6edf3;
            }
            .deploy-detail {
                font-size: 11px;
                color: #8b949e;
                margin-top: 4px;
            }

            /* ===== SECTION HEADERS ===== */
            .section-header {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 10px 0;
                margin-bottom: 6px;
                border-bottom: 2px solid #21262d;
            }
            .section-header-icon {
                font-size: 22px;
            }
            .section-header-text {
                font-family: 'Inter', sans-serif;
                font-size: 18px;
                font-weight: 600;
                color: #e6edf3;
                margin: 0;
            }

            /* ===== METRIC BOX ===== */
            .metric-box {
                background: linear-gradient(145deg, #161b22, #1c2333);
                border: 1px solid #21262d;
                border-radius: 8px;
                padding: 14px;
                text-align: center;
            }
            .metric-value {
                font-family: 'JetBrains Mono', monospace;
                font-size: 28px;
                font-weight: 700;
                color: #4fc3f7;
            }
            .metric-label {
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                color: #8b949e;
                margin-top: 4px;
            }

            /* ===== BUTTON OVERRIDES ===== */
            .stButton > button {
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
                border-radius: 6px !important;
                border: 1px solid #30363d !important;
                background: linear-gradient(145deg, #21262d, #30363d) !important;
                color: #e6edf3 !important;
                transition: all 0.3s ease !important;
            }
            .stButton > button:hover {
                border-color: #4fc3f7 !important;
                box-shadow: 0 0 10px rgba(79, 195, 247, 0.2) !important;
                color: #4fc3f7 !important;
            }

            /* Rollback danger button */
            .rollback-btn .stButton > button {
                background: linear-gradient(145deg, #3d1a1a, #4a1e1e) !important;
                border-color: #f85149 !important;
                color: #f85149 !important;
            }
            .rollback-btn .stButton > button:hover {
                background: linear-gradient(145deg, #5a2020, #6b2525) !important;
                box-shadow: 0 0 15px rgba(248, 81, 73, 0.3) !important;
            }

            /* ===== SCROLLBAR ===== */
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: #0d1117; }
            ::-webkit-scrollbar-thumb {
                background: #30363d;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover { background: #484f58; }

            /* ===== MISC ===== */
            .stSelectbox label,
            .stTextInput label,
            .stTextArea label {
                font-family: 'Inter', sans-serif !important;
                color: #c9d1d9 !important;
            }
            hr {
                border-color: #21262d !important;
            }

            /* Hide Streamlit branding */
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
        </style>
        """

    @staticmethod
    def section_header(icon: str, title: str) -> str:
        """Return HTML for a styled section header."""
        return f"""
        <div class="section-header">
            <span class="section-header-icon">{icon}</span>
            <p class="section-header-text">{title}</p>
        </div>
        """

    @staticmethod
    def status_badge(status: str, label: str | None = None) -> str:
        """Return HTML for a status badge."""
        display_label = label or status
        return f'<span class="status-badge status-{status}">{display_label}</span>'

    @staticmethod
    def metric_box(value: str | int, label: str) -> str:
        """Return HTML for a metric box."""
        return f"""
        <div class="metric-box">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """
