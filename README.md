# Prompt Literacy Lab

Prompt Literacy Lab is a small academic research prototype for studying prompt literacy, AI interaction quality, learning outcomes, and transfer of knowledge.

The app supports participant session logging, prompt attempt tracking, AI response logging, reflection journaling, confidence ratings, automatic metrics, CSV export, and a simple analytics dashboard.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── data/
├── exports/
└── docs/
    └── AAEL_framework_notes.md
```

## Features

- Landing page titled **Prompt Literacy Lab**
- Participant ID input
- Task description area
- Prompt attempt logging
- AI response logging
- Reflection journal prompts:
  - What changed?
  - Why did you change it?
  - What did you learn?
- Confidence rating before and after task
- Automatic metrics:
  - Number of prompt attempts
  - Average prompt length
  - Reflection word count
- CSV export of all session data
- Simple analytics dashboard using saved CSV data

## Setup

1. Create and activate a Python virtual environment.

   ```bash
   python -m venv .venv
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

## Run Locally

Start the Streamlit app with:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal, usually:

```text
http://localhost:8501
```

## Data Export

Saved sessions are written to:

```text
exports/prompt_literacy_lab_sessions.csv
```

The sidebar also provides a CSV download button after at least one session has been saved.

## Notes for Researchers

This is a beginner-friendly prototype, not a full production research platform. Before using it with real participants, consider adding informed consent language, anonymization procedures, secure storage, IRB/ethics review materials, and a data management plan.
