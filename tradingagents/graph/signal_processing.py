# TradingAgents/graph/signal_processing.py

from langchain_openai import ChatOpenAI

from tradingagents.utils.context_budget import budget_from_config, truncate_text_middle
from tradingagents.dataflows.config import get_config


class SignalProcessor:
    """Processes trading signals to extract actionable decisions."""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """Initialize with an LLM for processing."""
        self.quick_thinking_llm = quick_thinking_llm

    def process_signal(self, full_signal: str) -> str:
        """
        Process a full trading signal to extract the core decision.

        Args:
            full_signal: Complete trading signal text

        Returns:
            Extracted decision (BUY, SELL, or HOLD)
        """
        config = get_config()
        budget = budget_from_config(config)
        # Most signals are short, but guard against huge debate outputs.
        clamped_signal = truncate_text_middle(full_signal, budget.content_budget_tokens)

        messages = [
            (
                "system",
                "You are an efficient assistant designed to analyze paragraphs or financial reports provided by a group of analysts. Your task is to extract the investment decision: SELL, BUY, or HOLD. Provide only the extracted decision (SELL, BUY, or HOLD) as your output, without adding any additional text or information.",
            ),
            ("human", clamped_signal),
        ]

        return self.quick_thinking_llm.invoke(messages).content
