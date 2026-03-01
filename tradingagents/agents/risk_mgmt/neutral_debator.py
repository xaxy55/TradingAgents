import time
import json

from tradingagents.utils.context_budget import (
    budget_from_config,
    clamp_many_blocks,
    truncate_text_tail,
)
from tradingagents.dataflows.config import get_config


def create_neutral_debator(llm):
    def neutral_node(state) -> dict:
        config = get_config()
        budget = budget_from_config(config)

        risk_debate_state = state["risk_debate_state"]
        asset_type = state.get("asset_type", "stock")
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        clamped = clamp_many_blocks(
            [
                ("trader", trader_decision),
                ("market", market_research_report),
                ("sentiment", sentiment_report),
                ("news", news_report),
                ("fundamentals", fundamentals_report),
            ],
            total_tokens=max(1, budget.content_budget_tokens * 7 // 10),
        )
        trader_decision = clamped["trader"]
        market_research_report = clamped["market"]
        sentiment_report = clamped["sentiment"]
        news_report = clamped["news"]
        fundamentals_report = clamped["fundamentals"]
        history = truncate_text_tail(history, max(1, budget.content_budget_tokens * 2 // 10))
        current_risky_response = truncate_text_tail(
            current_risky_response, max(1, budget.content_budget_tokens // 10)
        )
        current_safe_response = truncate_text_tail(
            current_safe_response, max(1, budget.content_budget_tokens // 10)
        )

        # Add crypto-specific risk considerations
        crypto_guidance = ""
        if asset_type == "cryptocurrency":
            crypto_guidance = """

**CRYPTOCURRENCY BALANCED PERSPECTIVE:**
As you provide a balanced view on cryptocurrency:
- Acknowledge both the high-growth potential and significant downside risks
- Consider position sizing that accounts for volatility (e.g., smaller % of portfolio)
- Evaluate whether technical and sentiment signals align with each other
- Balance short-term trading opportunities against long-term hold considerations
- Consider dollar-cost averaging to mitigate timing risk in volatile markets
- Weigh the innovation potential against regulatory and security concerns
- Think about diversification within crypto assets if taking exposure"""

        prompt = f"""As the Neutral Risk Analyst, your role is to provide a balanced perspective, weighing both the potential benefits and risks of the trader's decision or plan. You prioritize a well-rounded approach, evaluating the upsides and downsides while factoring in broader market trends, potential economic shifts, and diversification strategies.{crypto_guidance} Here is the trader's decision:

{trader_decision}

Your task is to challenge both the Risky and Safe Analysts, pointing out where each perspective may be overly optimistic or overly cautious. Use insights from the following data sources to support a moderate, sustainable strategy to adjust the trader's decision:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
{"Company Fundamentals Report" if asset_type == "stock" else "Project Analysis"}: {fundamentals_report}
Here is the current conversation history: {history} Here is the last response from the risky analyst: {current_risky_response} Here is the last response from the safe analyst: {current_safe_response}. If there are no responses from the other viewpoints, do not hallucinate and just present your point.

Engage actively by analyzing both sides critically, addressing weaknesses in the risky and conservative arguments to advocate for a more balanced approach. Challenge each of their points to illustrate why a moderate risk strategy might offer the best of both worlds, providing growth potential while safeguarding against extreme volatility. Focus on debating rather than simply presenting data, aiming to show that a balanced view can lead to the most reliable outcomes. Output conversationally as if you are speaking without any special formatting."""

        response = llm.invoke(prompt)

        argument = f"Neutral Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": neutral_history + "\n" + argument,
            "latest_speaker": "Neutral",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": argument,
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return neutral_node
