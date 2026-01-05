from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_news
from tradingagents.dataflows.config import get_config


def create_social_media_analyst(llm):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]
        asset_type = state.get("asset_type", "stock")

        tools = [
            get_news,
        ]

        base_system_message = (
            "You are a social media and company specific news researcher/analyst tasked with analyzing social media posts, recent company news, and public sentiment for a specific company over the past week. You will be given a company's name your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on this company's current state after looking at social media and what people are saying about that company, analyzing sentiment data of what people feel each day about the company, and looking at recent company news. Use the get_news(query, start_date, end_date) tool to search for company-specific news and social media discussions. Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
            + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
        )
        
        # Add cryptocurrency-specific guidance
        if asset_type == "cryptocurrency":
            crypto_guidance = """

**CRYPTOCURRENCY SOCIAL SENTIMENT ANALYSIS:**
You are analyzing social sentiment for a cryptocurrency. Crypto markets are heavily influenced by social media:
- **Twitter/X**: Major source of crypto news and sentiment. Track discussions, trending hashtags, influential crypto accounts
- **Reddit**: Communities like r/CryptoCurrency, r/Bitcoin, r/ethereum provide grassroots sentiment
- **Telegram/Discord**: Many crypto communities are active on these platforms (though you may have limited direct access)
- **Fear & Greed Index**: Crypto-specific sentiment indicators if mentioned in news
- **Developer Activity**: GitHub commits, technical discussions indicate project health
- **Influencer Impact**: Statements from crypto influencers can significantly move prices
- **Memes & Viral Content**: Particularly relevant for meme coins and retail sentiment
- **Community Sentiment**: Token holder sentiment, governance discussions

Key considerations:
1. Crypto social sentiment can be extremely volatile and change rapidly
2. Be aware of coordinated pump/dump schemes and manipulation
3. Distinguish between genuine community sentiment and astroturfing/bot activity
4. News spreads faster in crypto communities compared to traditional finance
5. FUD (Fear, Uncertainty, Doubt) and FOMO (Fear of Missing Out) are particularly strong in crypto"""
            system_message = base_system_message + crypto_guidance
        else:
            system_message = base_system_message

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "sentiment_report": report,
        }

    return social_media_analyst_node
