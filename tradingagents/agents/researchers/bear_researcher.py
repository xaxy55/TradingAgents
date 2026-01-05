from langchain_core.messages import AIMessage
import time
import json


def create_bear_researcher(llm, memory):
    def bear_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        asset_type = state.get("asset_type", "stock")
        history = investment_debate_state.get("history", "")
        bear_history = investment_debate_state.get("bear_history", "")

        current_response = investment_debate_state.get("current_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        # Adjust prompt based on asset type
        if asset_type == "cryptocurrency":
            asset_focus = "cryptocurrency"
            additional_guidance = """
**CRYPTOCURRENCY-SPECIFIC BEAR FACTORS:**
- Regulatory Risk: Potential bans, restrictions, or unfavorable regulations from governments
- Volatility Risk: Extreme price volatility can lead to significant losses
- Security Concerns: Exchange hacks, smart contract vulnerabilities, or wallet security issues
- Competition: Numerous alternative cryptocurrencies competing for market share
- Lack of Fundamentals: No traditional valuation metrics, making it difficult to assess intrinsic value
- Market Manipulation: Whale activity, pump-and-dump schemes, or coordinated manipulation
- Technology Risk: Blockchain scalability issues, technical failures, or superior competing technology
- Sentiment-Driven: Heavy reliance on hype and social sentiment rather than underlying value
- Environmental Concerns: For proof-of-work cryptocurrencies, energy consumption criticism"""
        else:
            asset_focus = "stock"
            additional_guidance = ""

        prompt = f"""You are a Bear Analyst making the case against investing in the {asset_focus}. Your goal is to present a well-reasoned argument emphasizing risks, challenges, and negative indicators. Leverage the provided research and data to highlight potential downsides and counter bullish arguments effectively.

Key points to focus on:

- Risks and Challenges: Highlight factors like market threats, instability, or macroeconomic concerns that could hinder performance.
- Competitive Weaknesses: Emphasize vulnerabilities such as declining positioning, innovation gaps, or competitive threats.
- Negative Indicators: Use evidence from technical analysis, sentiment data, or recent adverse news to support your position.
- Bull Counterpoints: Critically analyze the bull argument with specific data and sound reasoning, exposing weaknesses or over-optimistic assumptions.
- Engagement: Present your argument in a conversational style, directly engaging with the bull analyst's points and debating effectively rather than simply listing facts.{additional_guidance}

Resources available:

Market research report: {market_research_report}
Social media sentiment report: {sentiment_report}
Latest world affairs news: {news_report}
{"Company fundamentals report" if asset_type == "stock" else "Project analysis"}: {fundamentals_report}
Conversation history of the debate: {history}
Last bull argument: {current_response}
Reflections from similar situations and lessons learned: {past_memory_str}
Use this information to deliver a compelling bear argument, refute the bull's claims, and engage in a dynamic debate that demonstrates the risks and weaknesses of investing in the {asset_focus}. You must also address reflections and learn from lessons and mistakes you made in the past.
"""

        response = llm.invoke(prompt)

        argument = f"Bear Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bear_history": bear_history + "\n" + argument,
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bear_node
