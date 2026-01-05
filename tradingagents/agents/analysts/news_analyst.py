from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_news, get_global_news
from tradingagents.dataflows.config import get_config


def create_news_analyst(llm):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        asset_type = state.get("asset_type", "stock")

        tools = [
            get_news,
            get_global_news,
        ]

        base_system_message = (
            "You are a news researcher tasked with analyzing recent news and trends over the past week. Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. Use the available tools: get_news(query, start_date, end_date) for company-specific or targeted news searches, and get_global_news(curr_date, look_back_days, limit) for broader macroeconomic news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
            + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
        )
        
        # Add cryptocurrency-specific guidance
        if asset_type == "cryptocurrency":
            crypto_guidance = """

**CRYPTOCURRENCY-SPECIFIC NEWS ANALYSIS:**
You are analyzing news for a cryptocurrency asset. Focus on these unique news categories:
- **Regulatory Developments**: Government regulations, SEC announcements, legal decisions affecting crypto
- **Adoption News**: Major companies accepting crypto, institutional investment, ETF approvals
- **Technical Developments**: Network upgrades, protocol changes, hard forks, blockchain updates
- **Security Events**: Exchange hacks, wallet breaches, security vulnerabilities
- **Market Infrastructure**: Exchange listings/delistings, DeFi protocols, stablecoin news
- **Macro Factors**: Interest rates and monetary policy (affects risk assets including crypto)
- **Influential Figures**: Statements from major crypto figures, developers, and thought leaders
- **On-Chain Metrics**: Large transactions, whale movements, network activity changes

Pay special attention to:
1. Regulatory sentiment across different jurisdictions (US, EU, Asia)
2. News about the specific blockchain or protocol (e.g., Ethereum upgrades for ETH)
3. Broader crypto market sentiment (Bitcoin often affects other cryptocurrencies)
4. Traditional finance integration news (banks, payment processors, custody services)"""
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
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
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
            "news_report": report,
        }

    return news_analyst_node
