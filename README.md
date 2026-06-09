# AIFit

AIFit is a human-in-the-loop AI product decision tool for evaluating whether an AI feature should be built, narrowed, prototyped, or avoided.

It helps product teams assess AI Fit, Commercial Upside, Risk Burden, and Evidence Readiness, then generates a structured review and validation workflow.

## Why I built this
Many AI product discussions focus on capability and feasibility. I envisioned a tool that also considers risk, evidence quality, human review, and validation before deciding whether an AI feature should be built.

## What it does

## Evaluation framework

## Human review workflow

## Validation workflow

## Tech stack

## Prerequisites
Before running AIFit locally, make sure you have:

- Python 3.10 or later
- Git
- A virtual environment created for the project
- Required Python libraries installed from `requirements.txt`
- An OpenRouter API key stored in Streamlit secrets

## Local setup

```bash
# Clone the repo
git clone <your-repo-url>
cd ai-fit

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Create a local Streamlit secrets file:
mkdir -p .streamlit
touch .streamlit/secrets.toml

# Add your own openrouter api key:
OPENROUTER_API_KEY = "your_api_key_here"

# Do not commit .streamlit/secrets.toml to Github:
Also make sure `.gitignore` includes:

```text
.venv/
.streamlit/secrets.toml
__pycache__/

## Limitations

## Learning goals
