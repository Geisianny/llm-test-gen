# Investigating the Use of a Large Language Model for Acceptance Test Scenario Generation

This repository provides all scripts, configurations, and artifacts required to reproduce the experiment described in the study: *Investigating the Use of an LLM for Acceptance Test Scenario Generation*.

---

## ⚙️ Experimental Pipeline

The project implements a complete pipeline divided into the following stages:

| Step | Description |
|------|------------|
| 0-GitHubSearch | Search for repositories containing Gherkin |
| 1-downloader | Data collection |
| 2-ParserAndFiltering | Data cleaning and validation |
| 2.1-RandomSelection | Sample selection |
| 3-Characterization | User story characterization |
| 4-UsEvaluation | User story evaluation |
| 5-LLMsToTest | Scenario generation using LLMs |
| 6-FeatureEvaluation | Feature evaluation |
| 7-scenario_quality | Scenario quality evaluation |
| featuresEvaluationSummary | Results consolidation |

---

## 🚀 Setup & Execution

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the environment

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env_example .env
```

---


## 📁 Output Structure

Results are available in:

```bash
/output
```
