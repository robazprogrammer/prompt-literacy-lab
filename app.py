"""
Prompt Literacy Lab
A beginner-friendly Streamlit prototype for studying prompt literacy,
AI interaction quality, learning outcomes, and transfer of knowledge.

Run locally with:
    streamlit run app.py
"""

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Basic paths
# -----------------------------------------------------------------------------
DATA_DIR = Path("data")
EXPORT_DIR = Path("exports")
EXPORT_FILE = EXPORT_DIR / "prompt_literacy_lab_sessions.csv"

DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# Page setup and academic prototype styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Prompt Literacy Lab",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f7f4;
    }
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #25324d;
    }
    .study-card {
        background-color: #ffffff;
        border: 1px solid #d9d9d0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .metric-note {
        color: #555555;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def word_count(text: str) -> int:
    """Return a simple whitespace-based word count."""
    return len(text.split()) if text else 0


def calculate_metrics(prompt_text: str, reflection_text: str) -> dict:
    """Calculate automatic session metrics from prompt and reflection logs."""
    prompts = [line.strip() for line in prompt_text.splitlines() if line.strip()]
    prompt_lengths = [len(prompt.split()) for prompt in prompts]

    return {
        "number_of_prompt_attempts": len(prompts),
        "average_prompt_length": round(sum(prompt_lengths) / len(prompt_lengths), 2)
        if prompt_lengths
        else 0,
        "reflection_word_count": word_count(reflection_text),
    }


def build_session_record(
    participant_id: str,
    task_description: str,
    prompt_attempts: str,
    ai_responses: str,
    what_changed: str,
    why_changed: str,
    what_learned: str,
    confidence_before: int,
    confidence_after: int,
) -> dict:
    """Create one row of session data for export and analysis."""
    full_reflection = " ".join([what_changed, why_changed, what_learned])
    metrics = calculate_metrics(prompt_attempts, full_reflection)

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "participant_id": participant_id,
        "task_description": task_description,
        "prompt_attempts": prompt_attempts,
        "ai_responses": ai_responses,
        "reflection_what_changed": what_changed,
        "reflection_why_changed": why_changed,
        "reflection_what_learned": what_learned,
        "confidence_before": confidence_before,
        "confidence_after": confidence_after,
        "confidence_change": confidence_after - confidence_before,
        **metrics,
    }


def append_to_csv(record: dict, path: Path) -> None:
    """Append one session record to the CSV export file."""
    row = pd.DataFrame([record])
    if path.exists():
        row.to_csv(path, mode="a", header=False, index=False)
    else:
        row.to_csv(path, index=False)


def load_exports(path: Path) -> pd.DataFrame:
    """Load exported session data if available."""
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# App header
# -----------------------------------------------------------------------------
st.title("Prompt Literacy Lab")
st.subheader("Academic prototype for studying prompt design, reflection, and learning transfer")

st.info(
    "Use this prototype to record participant prompt attempts, AI responses, "
    "reflection notes, confidence ratings, and simple session-level metrics."
)


# -----------------------------------------------------------------------------
# Sidebar: participant and study controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Session Setup")
    participant_id = st.text_input("Participant ID", placeholder="Example: P001")

    st.markdown("---")
    st.caption("CSV export location")
    st.code(str(EXPORT_FILE))

    if EXPORT_FILE.exists():
        with open(EXPORT_FILE, "rb") as file:
            st.download_button(
                label="Download CSV export",
                data=file,
                file_name="prompt_literacy_lab_sessions.csv",
                mime="text/csv",
            )


# -----------------------------------------------------------------------------
# Main data collection form
# -----------------------------------------------------------------------------
st.header("Study Session Log")

with st.form("session_log_form", clear_on_submit=False):
    st.markdown('<div class="study-card">', unsafe_allow_html=True)
    task_description = st.text_area(
        "Task description area",
        placeholder="Describe the task participants are trying to complete.",
        height=100,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    confidence_col_1, confidence_col_2 = st.columns(2)
    with confidence_col_1:
        confidence_before = st.slider(
            "Confidence before task", min_value=1, max_value=5, value=3
        )
    with confidence_col_2:
        confidence_after = st.slider(
            "Confidence after task", min_value=1, max_value=5, value=3
        )

    st.markdown("### Prompt and AI Interaction Log")
    prompt_attempts = st.text_area(
        "Prompt attempt logging",
        placeholder="Enter each prompt attempt on a new line.",
        height=180,
    )
    ai_responses = st.text_area(
        "AI response logging",
        placeholder="Paste or summarize AI responses here.",
        height=180,
    )

    st.markdown("### Reflection Journal")
    reflection_col_1, reflection_col_2, reflection_col_3 = st.columns(3)
    with reflection_col_1:
        what_changed = st.text_area("What changed?", height=130)
    with reflection_col_2:
        why_changed = st.text_area("Why did you change it?", height=130)
    with reflection_col_3:
        what_learned = st.text_area("What did you learn?", height=130)

    submitted = st.form_submit_button("Save session to CSV")

if submitted:
    if not participant_id.strip():
        st.error("Please enter a Participant ID before saving the session.")
    else:
        session_record = build_session_record(
            participant_id=participant_id.strip(),
            task_description=task_description,
            prompt_attempts=prompt_attempts,
            ai_responses=ai_responses,
            what_changed=what_changed,
            why_changed=why_changed,
            what_learned=what_learned,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
        )
        append_to_csv(session_record, EXPORT_FILE)
        st.success("Session saved to CSV export.")


# -----------------------------------------------------------------------------
# Live metrics preview
# -----------------------------------------------------------------------------
st.header("Automatic Metrics Preview")
full_reflection_preview = " ".join([what_changed, why_changed, what_learned])
metrics = calculate_metrics(prompt_attempts, full_reflection_preview)

metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)
metric_col_1.metric("Prompt attempts", metrics["number_of_prompt_attempts"])
metric_col_2.metric("Avg. prompt length", metrics["average_prompt_length"])
metric_col_3.metric("Reflection words", metrics["reflection_word_count"])
metric_col_4.metric("Confidence change", confidence_after - confidence_before)

st.caption("Prompt length and reflection length are counted with simple whitespace-based word counts.")


# -----------------------------------------------------------------------------
# Simple analytics dashboard
# -----------------------------------------------------------------------------
st.header("Simple Analytics Dashboard")
exported_data = load_exports(EXPORT_FILE)

if exported_data.empty:
    st.warning("No saved sessions yet. Save a session to populate the dashboard.")
else:
    st.dataframe(exported_data, use_container_width=True)

    dash_col_1, dash_col_2, dash_col_3 = st.columns(3)
    dash_col_1.metric("Saved sessions", len(exported_data))
    dash_col_2.metric(
        "Mean prompt attempts",
        round(exported_data["number_of_prompt_attempts"].mean(), 2),
    )
    dash_col_3.metric(
        "Mean confidence change",
        round(exported_data["confidence_change"].mean(), 2),
    )

    chart_col_1, chart_col_2 = st.columns(2)
    with chart_col_1:
        st.markdown("#### Confidence Change by Session")
        st.bar_chart(exported_data["confidence_change"])
    with chart_col_2:
        st.markdown("#### Reflection Word Count by Session")
        st.line_chart(exported_data["reflection_word_count"])
