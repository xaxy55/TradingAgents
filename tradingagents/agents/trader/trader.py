import functools
import time
import json

from tradingagents.utils.context_budget import budget_from_config, truncate_text_middle
from tradingagents.dataflows.config import get_config


def create_trader(llm, memory):
    def trader_node(state, name):
        config = get_config()
        budget = budget_from_config(config)

        company_name = state["company_of_interest"]
        asset_type = state.get("asset_type", "stock")
        investment_plan = state["investment_plan"]
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        if past_memories:
            for i, rec in enumerate(past_memories, 1):
                past_memory_str += rec["recommendation"] + "\n\n"
        else:
            past_memory_str = "No past memories found."

        # Clamp potentially huge blocks.
        past_memory_str = truncate_text_middle(
            past_memory_str, max(1, budget.content_budget_tokens * 2 // 10)
        )
        investment_plan = truncate_text_middle(
            investment_plan, max(1, budget.content_budget_tokens * 6 // 10)
        )

        # Build context based on asset type
        if asset_type == "cryptocurrency":
            asset_description = f"cryptocurrency {company_name}"
            trading_guidance = """

**CRYPTOCURRENCY TRADING CONSIDERATIONS:**
- 24/7 Market: Unlike stocks, crypto trades continuously. Consider timing across global time zones
- High Volatility: Cryptocurrencies can move 10-20% or more in a day. Adjust position sizing accordingly
- Liquidity: Ensure the crypto has sufficient trading volume on major exchanges
- No Circuit Breakers: Crypto markets don't have trading halts like stock markets
- Regulatory Risk: Be conservative given potential regulatory announcements
- Technical Analysis: Often more relevant than fundamentals for crypto trading
- Sentiment-Driven: Social sentiment and news have outsized impact on crypto prices"""
        else:
            asset_description = f"company {company_name}"
            trading_guidance = ""

        context = {
            "role": "user",
            "content": f"Based on a comprehensive analysis by a team of analysts, here is an investment plan tailored for the {asset_description}. This plan incorporates insights from current technical market trends, macroeconomic indicators, and social media sentiment. Use this plan as a foundation for evaluating your next trading decision.\n\nProposed Investment Plan: {investment_plan}\n\nLeverage these insights to make an informed and strategic decision.{trading_guidance}",
        }

        messages = [
            {
                "role": "system",
                "content": f"""You are a trading agent analyzing market data to make investment decisions for a {asset_type}. Based on your analysis, provide a specific recommendation to buy, sell, or hold. End with a firm decision and always conclude your response with 'FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**' to confirm your recommendation. Do not forget to utilize lessons from past decisions to learn from your mistakes. Here is some reflections from similar situations you traded in and the lessons learned: {past_memory_str}""",
            },
            context,
        ]

        result = llm.invoke(messages)

        return {
            "messages": [result],
            "trader_investment_plan": result.content,
            "sender": name,
        }

    return functools.partial(trader_node, name="Trader")
