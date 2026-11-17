# ProcessShift — AI-assisted business process transformation

**A portfolio project for a junior AI-native management consulting role.**

**Business problem:** Invoice exceptions often bounce between accounts payable, operations and finance. Missing information, waiting, and rework can delay completion. The aim is to discover where the process stalls, propose practical changes, and help a human team run a measurable improvement pilot.

**What the prototype actually does:**
1. Loads a synthetic event log or your own compatible CSV.
2. Computes case-level lead times, rework, target breaches and cumulative waiting time between steps using transparent Python logic.
3. Translates observed patterns into **testable improvement hypotheses**, not unverified claims.
4. Optionally uses an OpenAI model to draft a management consulting memo from **aggregated data only**.
5. Builds a four-week change pilot and a **clearly illustrative** time/capacity value scenario.
6. Downloads an executive brief.

**What is not implemented:** Connecting to a real ERP, sending notifications, automatic approval, actual AI-agent tool use, deployment in a customer's environment, or measured business savings. This is a **prototype** with simulated events. AI memo generation requires a user-provided API key and API access; the rest runs without one.

## Run locally

Requirements: Python 3.10+ and an internet connection once to install dependencies.

```bash
cd brightshift_process_copilot
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

To run basic tests (no dependencies):

```bash
python -m unittest discover -p "test_*.py" -v
```

## Demo walkthrough (2–3 minutes)

1. Open the Diagnose tab: show how 36 fictional invoices have different lead times and handoffs.
2. Open Root-cause hypotheses: identify missing handover information and rework, while being explicit that the data cannot prove causation.
3. Open AI consultant: demonstrate the aggregate-data prompt and, with a valid API key, generate an AI briefing. Without a key, show the deterministic analyst brief and explicitly state **no AI model was called**.
4. Open Pilot & business case: change the sliders to demonstrate assumptions and show how you'd measure **actual** improvements during a customer pilot.
5. Download the executive brief.

## Approach and safety

- **Deterministic analytics:** no fabricated AI classifications or model-generated KPIs.
- **AI integration:** optional OpenAI Responses API, generating recommendations only from computed aggregated metrics. The model never decides whether to pay an invoice.
- **Privacy:** vendor names, comments and invoice IDs are not sent to the API. Only synthetic or approved data should be used. The uploaded CSV is processed in the running Streamlit session.
- **Prompt injection / hallucination:** treat event log text as untrusted; verify any AI text against computed numbers. Review outputs before sharing.
- **Measurement honesty:** time intervals include nights/weekends. Saved time/cost scenarios are assumptions, not measured ROI; capacity gain is not necessarily cash savings.
- **Production next steps:** access control, real data governance, working-hours-aware cycle times, usability interviews, monitoring, baseline-versus-pilot design, and security review.

## Example application narrative

> I built ProcessShift to explore how AI can support organizational change, not simply automate content. I started with a business problem I knew from finance: invoice exceptions and ownership handoffs. The app measures process friction, proposes testable changes, asks humans to review recommendations, and provides a pilot plan with clearly labelled value assumptions. AI drafts a client-facing memo from aggregate statistics; it does not invent or approve financial decisions.

**Do not claim measured reductions or live customer adoption from this prototype.**

## Input schema

`case_id,activity,timestamp,team,amount_sek,vendor,note`

Timestamp format: `YYYY-MM-DD HH:MM`. Each row is a process event. A case should have two or more events for meaningful elapsed time. No real customer data is included.

## Suggested CV line (only once you've run and understood it)

**ProcessShift — AI-assisted business process diagnostic | Python, Streamlit, OpenAI API (optional)**  
Built a prototype analyzing invoice-event logs to flag process delays and rework, propose human-reviewed improvements, and prepare an AI-assisted transformation pilot and scenario-based value estimate.
