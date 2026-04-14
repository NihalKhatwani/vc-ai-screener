"""Core generation logic for the AI secondaries deal screener."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from prompts import ANALYSIS_SYSTEM_PROMPT, build_analysis_prompt, build_markdown_prompt


class Scorecard(BaseModel):
    """Lightweight scorecard for first-pass screening."""

    asset_quality: int = Field(ge=1, le=5)
    manager_quality: int = Field(ge=1, le=5)
    diversification: int = Field(ge=1, le=5)
    pricing: int = Field(ge=1, le=5)
    downside_protection: int = Field(ge=1, le=5)
    overall: int = Field(ge=1, le=5)


class SecondariesAnalysis(BaseModel):
    """Structured first-pass analysis for a secondaries opportunity."""

    opportunity_name: str
    one_line_summary: str
    transaction_type: str
    seller_type: str
    manager_sponsor: str
    portfolio_asset: str
    strategy: str
    geography: str
    vintage_exposure: str
    remaining_unfunded_commitments: str
    preliminary_recommendation: str
    memo_confidence: str
    deal_summary: str
    seller_motivation: str
    portfolio_asset_snapshot: str
    top_exposures: list[str]
    quality_signals: list[str]
    pricing_observations: list[str]
    structuring_considerations: list[str]
    concentration_risks: list[str]
    bull_case: list[str]
    bear_case: list[str]
    red_flags: list[str]
    diligence_questions: list[str]
    analyst_view: str
    scorecard: Scorecard


class GenerationOutputs(BaseModel):
    """Combined structured and markdown outputs."""

    analysis: SecondariesAnalysis
    markdown: str


class SecondariesMemoGenerator:
    """Generate structured analysis and markdown memo from raw secondaries notes."""

    def __init__(self, model: str = "gpt-5") -> None:
        load_dotenv()
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Add it to your environment or .env file.")
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        *,
        deal_brief: str,
        fund_lens: str | None = None,
        partner_questions: str | None = None,
    ) -> GenerationOutputs:
        """Generate both JSON analysis and markdown memo."""
        analysis = self._generate_analysis(
            deal_brief=deal_brief,
            fund_lens=fund_lens,
            partner_questions=partner_questions,
        )
        markdown = self._generate_markdown(analysis)
        return GenerationOutputs(analysis=analysis, markdown=markdown)

    def _generate_analysis(
        self,
        *,
        deal_brief: str,
        fund_lens: str | None,
        partner_questions: str | None,
    ) -> SecondariesAnalysis:
        prompt = build_analysis_prompt(
            deal_brief=deal_brief,
            fund_lens=fund_lens,
            partner_questions=partner_questions,
        )
        response = self.client.responses.create(
            model=self.model,
            instructions=ANALYSIS_SYSTEM_PROMPT,
            input=prompt,
        )
        raw_text = response.output_text
        payload = _extract_json_object(raw_text)
        return SecondariesAnalysis.model_validate(payload)

    def _generate_markdown(self, analysis: SecondariesAnalysis) -> str:
        prompt = build_markdown_prompt(analysis.model_dump())
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text.strip()



def save_outputs(output_dir: str | os.PathLike[str], outputs: GenerationOutputs) -> tuple[Path, Path]:
    """Write structured analysis and markdown memo to disk."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    slug = _slugify(outputs.analysis.opportunity_name) or "secondaries_opportunity"
    json_path = output_path / f"{slug}_analysis.json"
    memo_path = output_path / f"{slug}_memo.md"

    json_path.write_text(
        json.dumps(outputs.analysis.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    memo_path.write_text(outputs.markdown, encoding="utf-8")
    return json_path, memo_path



def _extract_json_object(text: str) -> dict[str, Any]:
    """Extract a JSON object from model output, including fenced code blocks."""
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    candidate = fenced.group(1) if fenced else text.strip()

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model did not return valid JSON.")
        return json.loads(candidate[start : end + 1])



def _slugify(value: str) -> str:
    """Convert a title into a filesystem-friendly slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")
