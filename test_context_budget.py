#!/usr/bin/env python3
"""Sanity checks for prompt budgeting utilities.

These tests are intentionally lightweight and do not require network access.
"""

from tradingagents.utils.context_budget import (
    estimate_tokens,
    truncate_text_middle,
    truncate_text_tail,
    clamp_many_blocks,
    PromptBudget,
)


def test_truncate_middle_respects_budget():
    text = "A" * 200000
    out = truncate_text_middle(text, max_tokens=1000)
    assert estimate_tokens(out) <= 1100  # heuristic variance
    assert "<truncated>" in out


def test_truncate_tail_keeps_end():
    text = "start\n" + ("x" * 10000) + "\nEND"
    out = truncate_text_tail(text, max_tokens=200)
    assert out.strip().endswith("END")


def test_clamp_many_blocks_total_budget():
    blocks = [("a", "A" * 50000), ("b", "B" * 50000), ("c", "C" * 50000)]
    clamped = clamp_many_blocks(blocks, total_tokens=1500)
    joined = "\n\n".join(clamped.values())
    assert estimate_tokens(joined) <= 1700  # heuristic variance


def test_prompt_budget_math():
    b = PromptBudget(max_input_tokens=12000, reserved_output_tokens=2048)
    assert b.content_budget_tokens == 9952


if __name__ == "__main__":
    # Allow running without pytest
    test_truncate_middle_respects_budget()
    test_truncate_tail_keeps_end()
    test_clamp_many_blocks_total_budget()
    test_prompt_budget_math()
    print("OK")
