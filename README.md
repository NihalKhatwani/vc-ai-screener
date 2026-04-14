# AI Secondaries Deal Screener

A lightweight AI-assisted workflow for **mid-market private equity secondaries screening**.

This project takes a deal teaser, LP portfolio summary, continuation vehicle note, or messy diligence notes and turns them into a **first-pass secondaries screening memo** with:

- transaction type and seller motivation
- portfolio or asset snapshot
- top exposures and concentration flags
- pricing observations
- structuring considerations
- red flags and data gaps
- diligence questions
- an initial recommendation

It is designed to feel like actual **secondaries investing internship work**, not a generic chatbot demo.

---

## Why this project is relevant for a mid-market secondaries fund

A secondaries investor is not underwriting a seed-stage startup from scratch. The work is much more about:

- screening deal teasers quickly
- distinguishing LP-led from GP-led opportunities
- understanding seller motivation and liquidity context
- summarizing portfolio composition and concentration
- pressure-testing pricing support and downside
- surfacing diligence gaps before deeper work starts

This repo is built around exactly that workflow.

The model does the first-pass structuring. The analyst still owns:

- what source materials are trustworthy
- whether pricing is actually compelling
- how much concentration risk is acceptable
- whether the sponsor is high quality and aligned
- whether the deal fits the fund's mandate

That is the right way to talk about AI in a secondaries interview: **a synthesis tool, not an underwriting substitute**.

---

## What the app does

### Input
You paste in:
- a secondaries teaser
- an LP portfolio summary
- a continuation vehicle memo
- manager notes
- optional fund mandate or lens
- optional partner / IC questions

### Output
The app generates:
- a structured analysis JSON file
- a polished markdown screening memo you can edit and export

### Delivery surfaces
- **CLI** for fast demos and reproducible outputs
- **Streamlit app** for a cleaner presentation during interviews

---

## Repo structure

```text
secondaries_ai_screener/
├── app.py
├── generate_memo.py
├── memo_generator.py
├── prompts.py
├── requirements.txt
├── .env.example
├── .gitignore
├── INTERVIEWER_NOTE.txt
├── PARTNER_QUESTIONS_EXAMPLE.txt
├── examples/
│   └── deal_teaser_project_northbridge.txt
└── outputs/
    ├── project_northbridge_analysis.json
    └── project_northbridge_memo.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd secondaries_ai_screener
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then fill in:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5
```

---

## Quickstart

### Run the CLI demo
```bash
python generate_memo.py \
  --input examples/deal_teaser_project_northbridge.txt \
  --output-dir outputs
```

This will generate:
- `outputs/project_northbridge_analysis.json`
- `outputs/project_northbridge_memo.md`

### Run the Streamlit app
```bash
streamlit run app.py
```

Then paste a teaser or summary into the app and click **Generate memo**.

## Example output sections

The generated memo includes:
- Snapshot
- Deal Summary
- Seller Motivation
- Portfolio / Asset Snapshot
- Top Exposures
- Quality Signals
- Pricing Observations
- Structuring Considerations
- Concentration Risks
- Bull Case / Bear Case
- Red Flags
- Diligence Questions
- Scorecard

---

## What this project does **not** do

It does not:
- pull live market data
- replace legal or accounting diligence
- calculate a real valuation model
- make an investment decision for you

