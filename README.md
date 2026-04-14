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

---

## Example workflow

### 1. Collect raw inputs
Good source material includes:
- a teaser or CIM excerpt
- a portfolio summary from the seller or GP
- a continuation vehicle note
- manager track record notes
- concentration data
- your own diligence observations

### 2. Ask the model to structure the opportunity
The model extracts:
- transaction type
- seller motivation
- portfolio snapshot
- quality signals
- pricing observations
- concentration risks
- diligence gaps

### 3. Review the memo like an investor
Do **not** send the raw output without editing it.

You should tighten:
- the pricing view
- what the real downside case is
- how much concentration the fund can actually absorb
- whether the sponsor deserves the benefit of the doubt
- whether the deal deserves more work or should be parked

---

## Included example

The repository includes a fictional sample opportunity:

**Project Northbridge**  
A GP-led continuation vehicle for a vertical software company serving insurance compliance workflows.

The included files are:
- `examples/deal_teaser_project_northbridge.txt`
- `outputs/project_northbridge_analysis.json`
- `outputs/project_northbridge_memo.md`

This is intentionally fictional so you can show the workflow without making unsupported claims about a real deal.

---

## How to talk about this project in an interview

A strong explanation is:

> I rebuilt one of my AI projects around a secondaries workflow instead of a generic startup memo. It takes a teaser or continuation vehicle summary and turns it into a first-pass screening memo with structure, seller motivation, concentration flags, pricing questions, and diligence gaps. The point was not to automate investment decisions, but to speed up early synthesis so more time can go to actual underwriting.

Good points to emphasize:
- you chose a workflow that maps directly to a secondaries investing seat
- you understand the difference between LP-led and GP-led opportunities
- you treat AI as a drafting and structuring tool, not the final decision-maker
- you can explain every output section in investment terms
- you know where human judgment still matters most: pricing, downside, and manager quality

---

## Best ways to use this with an interviewer

### Option 1: Send the repo + sample memo
Send:
- GitHub link
- generated sample memo
- the short note in `INTERVIEWER_NOTE.txt`

### Option 2: Record a 90-second walkthrough
Show:
- the raw teaser text
- the app generating the memo
- the final memo output
- two places where you would still edit the output manually

### Option 3: Tailor it to the actual fund
Before sending, replace the sample brief with:
- a fictional LP-led portfolio sale, or
- a fictional GP-led continuation vehicle that looks closer to the fund's sweet spot

That makes the project feel much more intentional.

---

## CLI usage

### Basic
```bash
python generate_memo.py --input examples/deal_teaser_project_northbridge.txt --output-dir outputs
```

### With a fund lens and partner questions
```bash
python generate_memo.py \
  --input examples/deal_teaser_project_northbridge.txt \
  --fund-lens-file PARTNER_QUESTIONS_EXAMPLE.txt \
  --questions-file PARTNER_QUESTIONS_EXAMPLE.txt \
  --output-dir outputs
```

## Before you commit to GitHub
- Make sure `.env` is **not** committed. Only keep `.env.example`.
- Keep the included sample clearly fictional.
- Verify the app runs locally with `streamlit run app.py`.
- Verify the CLI runs locally with the sample file.
- Read the memo and note once in your own voice so you can defend every line in an interview.
```bash
python generate_memo.py --input examples/deal_teaser_project_northbridge.txt
```

### With a fund lens and IC questions
```bash
python generate_memo.py \
  --input examples/deal_teaser_project_northbridge.txt \
  --fund-lens-file your_fund_lens.txt \
  --questions-file PARTNER_QUESTIONS_EXAMPLE.txt \
  --output-dir outputs
```

### Optional inputs you can create
`your_fund_lens.txt`
```text
We like mid-market secondaries with seasoned assets, strong sponsor alignment, disciplined entry pricing, and a clear path to downside protection.
```

---

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

It is a **first-pass memo generator**, which is exactly why it is credible.

---

## Practical suggestions before you send it

1. Rename the sample opportunity if you want something cleaner.
2. Edit the sample memo by hand for one or two sharper investment points.
3. Push the repo to GitHub with a clean commit history.
4. Send the repo together with the sample memo, not the repo alone.
5. Be ready to explain what AI did and what you did.

---

## Suggested note to accompany the project

A clean version is:

Hi [Name] — I realized my existing AI projects were more technical than investing-specific, so I rebuilt one around a secondaries workflow instead.

It takes a secondaries teaser or continuation vehicle summary and turns it into a first-pass screening memo with transaction structure, seller motivation, concentration flags, pricing questions, and diligence gaps.

I thought this was a better representation of how I would actually use AI in an investing internship context, so I included the repo and a sample memo.

---

## Final framing

The strongest way to present this project is:

**I used AI to speed up synthesis of messy secondaries materials, while keeping the actual investment judgment human.**
# vc-ai-screener
