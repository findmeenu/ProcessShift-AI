# ProcessShift 2.0

**Business process diagnostics, invoice exception handling, and technology investment analysis**  
Python · Streamlit · Pandas · Optional generative AI (Gemini / OpenAI)

## Why I built it

When a business process is slow, introducing AI is not necessarily the right first move. I built ProcessShift to examine the workflow before recommending a solution: where do invoices get delayed, what could explain the delays, and would process redesign, conventional automation, or AI deliver the best value?

ProcessShift is an interactive **portfolio prototype**, using a synthetic invoice-processing workflow. It combines event-log analysis, rule-based invoice checks, optional AI-generated writing, and an editable investment model. The goal is to make the reasoning behind a recommendation visible—not to assume AI is the answer.

> **Scope:** This is an independent synthetic case study, not a client engagement or deployed ERP solution. Financial benefits are modeled assumptions, not realized savings.

## Features: all eight application tabs

### 1. 📊 Diagnose — understand the current process

- Load the included synthetic event log or upload another compatible CSV.
- Calculate number of cases, median elapsed lead time, percentage beyond the target, and cases with repeated activities (rework).
- Explore charts of cumulative time between process steps and case-level completion times.
- Inspect the underlying event-to-event gap table as an audit trail.

**Interpretation:** Lead time is wall-clock elapsed time between events. A long handoff is a signal to investigate, not proof of a team's responsibility or active working time.

### 2. 🧩 Root-cause hypotheses — turn findings into testable ideas

- Generate rule-based improvement hypotheses from event-log patterns.
- For each hypothesis, show the finding, suggested process change, human checkpoint, and pilot KPI.
- Distinguish observed delays from unverified explanations; confirm causes through interviews and process observation.

### 3. 🤖 AI consultant — draft a change memo

- Optionally use a supported generative-AI provider to draft a consultant-style change memo based on summarized process metrics.
- Review the draft and download the resulting memo.
- Keep business judgments and decisions with a human reviewer; the AI output is a draft, not independent evidence.

**API access:** An API key is needed only for AI-generated text. The deterministic analysis and financial tools work without one. Do not enter confidential client information or publish keys.

### 4. 📋 Pilot & business case — plan a controlled experiment

- Follow a four-week outline: discover and validate the baseline; trial a checklist and human-reviewed queue; measure and adapt.
- Adjust illustrative manual handling time and expected reduction to estimate monthly hours freed and potential monthly/annual capacity value.
- Review governance checkpoints for data quality, security approval, human financial approval, AI error monitoring, and adoption.
- Download a text-based executive brief.

**Interpretation:** Freed staff capacity does not automatically translate into lower cash expenditure.

### 5. 🧾 Invoice AI Assistant — check a single invoice

- Enter an invoice number, purchase order number, responsible owner, and optional exception details.
- Use deterministic rules to flag missing required information.
- Optionally generate a clarification draft for missing information.
- Edit the message, explicitly approve it, and then download the approved draft.

**Safety boundary:** The prototype does not send emails, approve invoices, or make payments.

### 6. 📁 Bulk Invoice Processing — validate multiple invoices

- Download an example invoice CSV or upload your own fictional/authorized sample.
- Check required fields across up to **500 invoices** and display validation results.
- Download the validation/exception results as CSV.
- Optionally generate clarification drafts for incomplete records.
- Review and edit individual drafts, approve selected messages, and export approved clarifications as CSV.

The bulk invoice input is **different** from the process event log. See the input formats below.

### 7. 📈 Automation Impact — explore operational value

- Reuse the invoice CSV uploaded in **Bulk Invoice Processing**.
- Display counts of checked, complete, and incomplete invoices and the observed missing-field rate for that uploaded file.
- Change assumptions for manual versus automated validation and clarification times.
- Estimate potential time saved, capacity value, and the contribution of different activities.
- Download a business impact report.

**Interpretation:** Counts come from the uploaded records; time savings and financial values are estimates. The dashboard does not demonstrate real-world ROI.

### 8. 🎯 Investment Strategy — choose what to pilot

- Connect synthetic event-log observations to a technology investment question.
- Compare **process redesign**, **rules-based automation**, and **AI-assisted automation**.
- Edit invoice volume, handling time, labor cost, error/exception assumptions, discount rate, and evaluation horizon (1–5 years).
- Edit each option's setup costs, annual license/API costs, support costs, minutes saved, adoption, and residual exception rate.
- Calculate annual capacity value, avoided-error value, net benefit, **NPV**, **undiscounted ROI**, and simple payback.
- Display the highest-positive-NPV option as a **provisional** model result; show no-investment guidance when none has positive modeled NPV.
- Compare conservative, base, and optimistic scenarios.
- Display a reproducible **12-case synthetic fixture evaluation** of the deterministic required-field detector, including false negatives.
- Export an investment decision brief (`.txt`) and option comparison (`.csv`).

**Example insight:** Under the included illustrative assumptions, rules-based automation leads on base-case modeled NPV, while process redesign is more resilient in the conservative case. This is a scenario-dependent finding, not a universal technology recommendation.

## Financial model: how the estimates work

The investment tab compares incremental benefits against one-time and recurring costs:

```text
Annual capacity value = monthly invoices × 12 × minutes saved × adoption
                        ÷ 60 × staff hourly cost

Annual avoided-error value = monthly invoices × 12
                             × max(0, baseline error rate − residual error rate)
                             × adoption × cost per error

Annual net benefit = annual capacity value + annual avoided-error value
                     − annual license/API cost − annual support cost

NPV = −setup cost + sum(annual net benefit / (1 + discount rate)^year)

ROI (%) = (total undiscounted benefit − total cost) / total cost × 100

Simple payback (months) = setup cost / annual net benefit × 12
                          (only when annual net benefit > 0)
```

The model caps minutes saved at the assumed baseline handling time. The conservative scenario uses 70% of base invoice volume and 70% of expected adoption; the optimistic scenario uses 130% volume and 110% adoption, capped at 100%. Costs stay unchanged in these scenarios.

The assumptions are editable and **have not been measured in a real organization**. Positive NPV is not investment approval; it identifies a hypothesis worth validating.

## Run the application locally

**Requirements:** Python 3.10+ and an internet connection only if you choose to call an AI provider.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit displays a local URL (usually `http://localhost:8501`). If the port is occupied, it may use another port.

The app opens with the included synthetic event log. **No API key is required** for process analysis, rule-based invoice validation, impact scenarios, investment comparisons, or synthetic fixture evaluation. For optional AI memo/clarification generation, select a supported provider and supply a valid key in the application. Never commit keys or secrets to GitHub.

### Input CSV formats

**Process event log** (for *Diagnose* and related workflow analysis):

```csv
case_id,activity,timestamp,team,amount_sek,vendor,note
```

- `timestamp` format: `YYYY-MM-DD HH:MM`.
- Start with `demo_invoices.csv`; regenerate synthetic events using `python generate_demo.py` if needed.

**Bulk invoice validation** (for *Bulk Invoice Processing* and *Automation Impact*):

```csv
invoice_number,po_number,owner
INV-101,,Sarah
INV-102,PO-200,John
INV-103,PO-201,
```

- Blank required fields are treated as missing.
- Use the sample CSV download in Tab 6 for the exact template.
- The demo accepts at most 500 invoice rows per upload.

## Testing and validation

Run the included automated tests:

```bash
python -m unittest discover -p "test_*.py" -v
```

- `test_engine.py` covers core workflow-analysis behavior.
- `test_strategy.py` covers investment-model behavior.
- `validation.py` evaluates the deterministic required-field detector on **12 manually labeled synthetic fixtures**.

**Do not interpret fixture accuracy as ML model accuracy or production performance.** The test does not measure AI draft quality, real-world invoice correctness, fraud detection, or security.

## Project structure

```text
ProcessShift/
├── app.py                 # Streamlit interface: eight tabs
├── engine.py              # Event-log analysis and process hypotheses
├── strategy.py            # Investment alternatives, NPV/ROI, scenarios
├── validation.py          # Synthetic required-field fixture evaluation
├── generate_demo.py       # Synthetic event-log generator
├── demo_invoices.csv      # Included synthetic event data
├── test_engine.py         # Core tests
├── test_strategy.py       # Investment tests
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── docs/                  # Optional consulting case study
```

## Consulting case study

I prepared a two-page case study to explain the investment decision, the trade-offs among three alternatives, and how I would test the recommendation before a real rollout. If you add the document to `docs/`, it can be reviewed alongside the source code.

## What this project demonstrates

- **Business analysis:** turning process data into questions, hypotheses, and measurable pilot KPIs.
- **Technology judgment:** comparing process changes and traditional automation with AI, rather than assuming the newest technology wins.
- **Technical implementation:** building an interactive Python/Streamlit application with deterministic rules, financial calculations, and optional generative-AI assistance.
- **Responsible delivery:** explicit assumptions, human review, reproducible tests, and clear boundaries between synthetic evidence and actual business results.

## Limitations and possible next steps

This prototype has **no live ERP integration**, does not send emails or approve payments, and has not been deployed or evaluated using client data. Event timestamps can include evenings/weekends; observed process gaps do not establish root causes. The synthetic fixture test is narrow, and AI-generated drafts require separate quality, privacy, and reliability evaluation.

Before production use, I would validate the baseline with process owners, test against authorized real data, assess information security and integrations, and run a controlled pilot measuring actual handling time, exception rates, employee adoption, and cost.
