"""CLI entrypoint for generating a secondaries screening memo."""

from __future__ import annotations

import argparse
from pathlib import Path

from memo_generator import SecondariesMemoGenerator, save_outputs


def read_optional_text(path_str: str | None) -> str | None:
    """Read optional text content from a file path."""
    if not path_str:
        return None
    return Path(path_str).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate an AI-assisted secondaries screening memo from a deal teaser or portfolio notes."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a text or markdown file containing the deal teaser, portfolio summary, or notes.",
    )
    parser.add_argument(
        "--fund-lens-file",
        help="Optional path to a file containing the fund's investment lens or mandate.",
    )
    parser.add_argument(
        "--questions-file",
        help="Optional path to a file containing investment committee or partner questions to prioritize.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory where the JSON and markdown memo will be written.",
    )
    parser.add_argument(
        "--model",
        default="gpt-5",
        help="Model name to send to the OpenAI API.",
    )
    return parser


def main() -> None:
    """Run the CLI workflow."""
    parser = build_parser()
    args = parser.parse_args()

    deal_brief = Path(args.input).read_text(encoding="utf-8")
    fund_lens = read_optional_text(args.fund_lens_file)
    partner_questions = read_optional_text(args.questions_file)

    generator = SecondariesMemoGenerator(model=args.model)
    outputs = generator.generate(
        deal_brief=deal_brief,
        fund_lens=fund_lens,
        partner_questions=partner_questions,
    )

    json_path, memo_path = save_outputs(args.output_dir, outputs)

    print("Generated files:")
    print(f"- JSON analysis: {json_path}")
    print(f"- Markdown memo: {memo_path}")


if __name__ == "__main__":
    main()
