# ProcessShift — AI-Assisted Business Process Improvement & Automation

**From workflow bottlenecks to actionable recommendations, human-reviewed AI drafts, and transparent business-impact estimates.**

**Live demo:** [Add your Streamlit Community Cloud URL here]  
**Source code:** https://github.com/findmeenu/ProcessShift-AI

> **Portfolio prototype** built with synthetic demonstration data. It does not connect to a live accounting system, send emails, approve payments, or demonstrate verified cost savings.

## The business problem

Invoice workflows can get stuck because information is missing, a handoff is unclear, or approval takes longer than expected. Manual follow-ups create repeated work, and managers may not know which step needs improvement.

ProcessShift demonstrates an approach to this problem: **measure workflow friction, propose testable changes, help employees handle invoice exceptions, and estimate potential business value**.

## What the application does

| Feature | What it demonstrates |
| --- | --- |
| **1. Diagnose** | Analyzes timestamped invoice events, lead times, target breaches, rework, and time between workflow steps. |
| **2. Root-cause hypotheses** | Converts observed patterns into possible explanations, proposed changes, human checkpoints, and KPIs. These are hypotheses, not proven causes. |
| **3. AI consultant** | Uses Google Gemini (or optionally OpenAI) to draft a consulting-style improvement memo based on aggregated metrics. Requires a user-provided API key. |
| **4. Pilot & business case** | Presents a change pilot and scenario-based value estimates using adjustable assumptions. |
| **5. Invoice AI Assistant** | Checks a single invoice for missing required fields and uses Gemini to draft a clarification request for employee review and approval. |
| **6. Bulk Invoice Processing** | Checks up to 500 invoice rows in an uploaded CSV, creates AI clarification templates by missing-field pattern, and exports only employee-approved drafts. |
| **7. Automation Impact** | Shows validated invoice counts, scenario-based time savings, and estimated labor value with adjustable assumptions; exports an impact CSV. |

## Demo dataset and illustrative findings

The built-in event log contains **36 fictional invoice cases**. With the default 72-hour target, the demonstration reports:

- **Median completion time:** 58.5 hours
- **Cases beyond target:** 38.9%
- **Cases with rework:** 38.9%
- **Cases with missing information:** 33.3%
- **Cumulative approval transition time:** 1,256 hours across cases

These findings describe **synthetic test data**, not a real organization's performance. Cumulative waiting time is not the same as employee working time.

The separate sample bulk-invoice CSV contains five rows: **two complete** and **three needing attention** under the demonstration rules.

## How the workflow works

1. **Inspect data:** Upload an event log or use the built-in demonstration data.
2. **Diagnose:** Python computes workflow measurements and flags patterns worth investigating.
3. **Recommend:** Rules generate testable hypotheses; an AI model can draft a management briefing from aggregate results.
4. **Assist:** Upload a separate bulk-invoice CSV. Python checks required fields and Gemini drafts clarification templates for missing information.
5. **Review:** A person edits and approves clarification drafts before downloading them. **Nothing is sent automatically.**
6. **Evaluate:** Adjust assumptions in the impact dashboard to illustrate a potential business case and define what should be measured in a real pilot.

## Tech stack

- **Python** — application logic and deterministic checks
- **Streamlit** — interactive web interface
- **Pandas** — CSV loading, validation, and analysis
- **Google Gemini API** — AI-generated recommendations and clarification drafts
- **OpenAI API** — optional alternative for the consulting memo

## Run locally

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the URL Streamlit displays in your terminal. The built-in workflow analysis works without an API key. For AI-generated outputs, select a provider in **AI consultant** and enter your **own** API key in the application's password field.

Run the included analytical tests:

```bash
python -m unittest discover -p "test_*.py" -v
```

## CSV inputs

**Event-log analysis (Diagnose):**

```text
case_id,activity,timestamp,team,amount_sek,vendor,note
```

Each row represents a workflow event; timestamps use `YYYY-MM-DD HH:MM`. The included `demo_invoices.csv` is an example.

**Bulk invoice validation:**

```text
invoice_number,po_number,owner
INV-101,,Sarah
INV-102,PO-200,John
INV-103,PO-201,
```

An empty required field is flagged for review. This is **field-presence validation**, not proof an invoice or PO is valid. The app supports a maximum of 500 rows per upload for this demo.

## Safety, privacy, and limitations

- **Human oversight:** AI-generated messages must be reviewed; the application does not send email, approve invoices, or initiate payments.
- **AI uncertainty:** Recommendations can be incorrect; staff must confirm root causes, policy requirements, and message accuracy.
- **Data minimization:** AI requests in the demonstrated workflows are designed to use aggregate findings or missing-field categories, not individual invoice identifiers or amounts. Review code and provider terms before using sensitive data.
- **Key security:** API keys are entered at runtime. **Never commit keys or private configuration files to GitHub.**
- **Impact estimates:** The dashboard combines actual counts from uploaded test files with **assumed** manual and automated handling times. It does not measure actual task duration or establish realized financial savings. Reductions in staff time do not necessarily become cash savings.
- **Scope:** There is no live ERP integration, email delivery, role-based access control, or production audit workflow. Use fictional or explicitly authorized data only.

## How I would validate the business value

A real pilot would first measure manual validation time, clarification drafting/review time, the rate of missing-information cases, and the time from exception detection to resolution. Then a limited group would use the assisted workflow while recording review time, corrections, failure cases, and staff feedback. Comparing both processes would help assess whether the automation truly reduces work without introducing quality or security problems.

## Next improvements

- Time the manual and AI-assisted workflows in controlled tests
- Add more realistic invoice rules and validation test cases
- Improve accessibility, errors, and input validation
- Add authentication, logging, and appropriate data-handling controls before any business use
- Evaluate optional integrations with existing ERP/ticketing systems

## Why I built it

My background combines finance operations, business-process improvement, and software development. I built ProcessShift to explore how AI can help teams **understand an operational problem, propose and test a practical improvement, keep people in control, and communicate potential business value**—rather than using AI simply to produce text.

**Project status:** Working portfolio prototype; not a production finance system.
