"""Streamlit app for the AI secondaries deal screener."""

from __future__ import annotations

import json

import streamlit as st

from memo_generator import SecondariesMemoGenerator

st.set_page_config(page_title="AI Secondaries Deal Screener", page_icon="📊", layout="wide")

st.title("📊 AI Secondaries Deal Screener")
st.caption(
    "Turn a deal teaser, portfolio summary, or continuation vehicle note into a first-pass "
    "secondaries screening memo with pricing questions, concentration flags, and diligence gaps."
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Model", value="gpt-5")
    st.markdown(
        "Use this as a first-pass analyst tool. Always review the output manually "
        "before sharing it internally."
    )

example_brief = """Opportunity name: Project Northbridge
Transaction type: GP-led continuation vehicle
Seller type: Existing LPs in Alder Ridge Capital Fund IV, with the sponsor leading a continuation process
Manager / sponsor: Alder Ridge Capital, a 2016-vintage mid-market buyout manager focused on vertical software and business services
Underlying asset: ComplianceCloud, a provider of regulatory workflow software for insurance brokers and carriers in the US and UK
What is being sold: A new continuation vehicle would acquire 92% of ComplianceCloud from Fund IV. Existing LPs can sell for cash or roll into the new vehicle.
Use of proceeds: LP liquidity plus a modest balance sheet reserve for tuck-in M&A and product expansion
Equity need: Lead buyer sought for approximately $180M, with the balance syndicated to existing and new investors
Valuation framing: Deal priced at 15.5x LTM EBITDA; sponsor argues public software peers and recent private transactions support 16.5x-18.0x for similar assets
Financials: FY2025 revenue of $78M, EBITDA of $26M, 17% revenue CAGR since 2022, 84% recurring revenue, 95% gross revenue retention, 111% net revenue retention
Growth plan: expand carrier-side modules, increase wallet share in existing broker accounts, and complete 1-2 tuck-in acquisitions over the next 24 months
Quality signals: mission-critical workflow product, low historical churn, strong cash conversion, sector with regulatory complexity and sticky compliance requirements
Concentration: single asset transaction; top 10 customers represent 28% of revenue, largest customer represents 6%
Geography: roughly 72% US, 28% UK
GP alignment: sponsor rolling 100% of carry and approximately 35% of gross proceeds into the continuation vehicle
Track record notes: prior Alder Ridge funds reported net multiples of 1.8x, 2.2x, and 1.9x; Fund IV currently marked at 1.6x gross MOIC
Current diligence gaps: no third-party QoE in the teaser, no detailed cohort churn by customer size, no product diligence materials yet, and limited information on the acquisition pipeline
Remaining unfunded commitments: none, other than a proposed reserve inside the continuation vehicle
Why seller is transacting: Fund IV is beyond its original hold period and the sponsor believes the asset still has runway for a longer ownership period
"""

col1, col2 = st.columns([1.15, 1])

with col1:
    deal_brief = st.text_area(
        "Deal teaser / portfolio summary / notes",
        value=example_brief,
        height=420,
        help="Paste in a secondaries teaser, continuation vehicle summary, fund portfolio notes, or your own synthesis.",
    )
    fund_lens = st.text_area(
        "Optional fund lens / mandate",
        placeholder="Example: We like mid-market secondaries with seasoned assets, strong sponsor alignment, and underwriting pathways to downside protection.",
        height=140,
    )
    partner_questions = st.text_area(
        "Optional IC / partner questions",
        placeholder="Example: Is pricing justified versus quality and concentration? What downside exists if growth slows and exit multiple compresses?",
        height=140,
    )
    generate = st.button("Generate memo", type="primary")

with col2:
    st.subheader("What this should produce")
    st.markdown(
        "- a crisp transaction summary\n"
        "- likely seller motivation and structure\n"
        "- concentration and downside flags\n"
        "- pricing and diligence questions a secondaries investor would ask\n"
        "- a first-pass recommendation"
    )

if generate:
    if not deal_brief.strip():
        st.error("Please paste a deal summary first.")
    else:
        try:
            generator = SecondariesMemoGenerator(model=model)
            with st.spinner("Generating memo..."):
                outputs = generator.generate(
                    deal_brief=deal_brief,
                    fund_lens=fund_lens,
                    partner_questions=partner_questions,
                )

            st.success("Memo generated.")

            memo_tab, json_tab = st.tabs(["Memo", "Structured JSON"])

            with memo_tab:
                st.markdown(outputs.markdown)
                st.download_button(
                    label="Download memo (.md)",
                    data=outputs.markdown,
                    file_name="secondaries_screening_memo.md",
                    mime="text/markdown",
                )

            with json_tab:
                json_payload = outputs.analysis.model_dump()
                st.json(json_payload)
                st.download_button(
                    label="Download analysis (.json)",
                    data=json.dumps(json_payload, indent=2),
                    file_name="secondaries_screening_analysis.json",
                    mime="application/json",
                )

        except Exception as exc:
            st.error(f"Generation failed: {exc}")
            st.info(
                "Check that your OPENAI_API_KEY is set in your environment or .env file, "
                "then try again."
            )
