from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence, Tuple


def _estimate_tokens_fallback(text: str) -> int:
    """Very rough token estimator.

    OpenAI/GPT-style tokenization averages ~3-4 chars/token for English.
    We deliberately err a bit high to be safer.
    """

    if not text:
        return 0
    return max(1, (len(text) + 2) // 3)


def estimate_tokens(text: str) -> int:
    """Estimate token count for text.

    Uses `tiktoken` if available; otherwise falls back to a conservative heuristic.
    """

    if not text:
        return 0

    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return _estimate_tokens_fallback(text)


def truncate_text_middle(text: str, max_tokens: int, *, marker: str = "\n...<truncated>...\n") -> str:
    """Truncate keeping start and end, removing the middle."""

    if max_tokens <= 0:
        return ""

    token_est = estimate_tokens(text)
    if token_est <= max_tokens:
        return text

    # If `tiktoken` is available, do an exact token-based truncation.
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        if len(tokens) <= max_tokens:
            return text

        marker_tokens = enc.encode(marker)
        available = max_tokens - len(marker_tokens)
        if available <= 0:
            # No room for marker + content; return a tail slice.
            return enc.decode(tokens[-max_tokens:])

        head_n = max(1, available // 2)
        tail_n = max(1, available - head_n)
        return enc.decode(tokens[:head_n]).rstrip() + marker + enc.decode(tokens[-tail_n:]).lstrip()
    except Exception:
        pass

    # Approximate by characters to avoid tokenization dependency.
    # Keep both head and tail with a marker.
    # Use a conservative chars-per-token so we don't overshoot.
    chars_budget = max(1, max_tokens * 3)
    if len(text) <= chars_budget:
        return text

    marker_len = len(marker)
    head_chars = max(1, (chars_budget - marker_len) // 2)
    tail_chars = max(1, chars_budget - marker_len - head_chars)

    return text[:head_chars].rstrip() + marker + text[-tail_chars:].lstrip()


def truncate_text_tail(text: str, max_tokens: int, *, marker: str = "\n...<truncated>...\n") -> str:
    """Truncate keeping the tail (most recent content)."""

    if max_tokens <= 0:
        return ""

    token_est = estimate_tokens(text)
    if token_est <= max_tokens:
        return text

    # If `tiktoken` is available, do an exact token-based truncation.
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        if len(tokens) <= max_tokens:
            return text

        marker_tokens = enc.encode(marker)
        available = max_tokens - len(marker_tokens)
        if available <= 0:
            return enc.decode(tokens[-max_tokens:])

        tail = enc.decode(tokens[-available:]).lstrip()
        return marker + tail
    except Exception:
        pass

    chars_budget = max(1, max_tokens * 3)
    if len(text) <= chars_budget:
        return text

    # Keep tail; include marker at start.
    tail_chars = max(1, chars_budget - len(marker))
    return marker + text[-tail_chars:].lstrip()


RoleContent = Tuple[str, str]


@dataclass(frozen=True)
class PromptBudget:
    """Input budgeting settings.

    - `max_input_tokens`: total budget for prompt *input* (not output).
    - `reserved_output_tokens`: tokens to reserve for the model output.

    Effective content budget is `max_input_tokens - reserved_output_tokens`.
    """

    max_input_tokens: int = 12000
    reserved_output_tokens: int = 2048

    @property
    def content_budget_tokens(self) -> int:
        return max(1, self.max_input_tokens - self.reserved_output_tokens)


def budget_from_config(config: Optional[dict[str, Any]] = None) -> PromptBudget:
    config = config or {}
    return PromptBudget(
        max_input_tokens=int(config.get("llm_max_input_tokens", 12000)),
        reserved_output_tokens=int(config.get("llm_reserved_output_tokens", 2048)),
    )


def clamp_many_blocks(blocks: Sequence[Tuple[str, str]], *, total_tokens: int) -> dict[str, str]:
    """Clamp a set of named prompt blocks into a shared total token budget.

    `blocks` is a list of (name, text). Returns dict[name] = clamped_text.

    Strategy:
    - Give each block an equal share, then (if heuristic variance) clamp the largest further.
    - Middle truncation is used to preserve both context and conclusions.
    """

    if total_tokens <= 0:
        return {name: "" for name, _ in blocks}

    if not blocks:
        return {}

    per_block = max(1, total_tokens // len(blocks))
    clamped: dict[str, str] = {}

    for name, text in blocks:
        clamped[name] = truncate_text_middle(text, per_block)

    joined = "\n\n".join(clamped.values())
    while estimate_tokens(joined) > total_tokens:
        biggest = max(clamped.items(), key=lambda kv: estimate_tokens(kv[1]))[0]
        clamped[biggest] = truncate_text_middle(
            clamped[biggest], max(1, estimate_tokens(clamped[biggest]) * 9 // 10)
        )
        joined = "\n\n".join(clamped.values())

    return clamped
