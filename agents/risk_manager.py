from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import AgentState
from tools.search import web_search

llm = ChatOpenAI(model="gpt-4o", temperature=0)

RISK_PROMPT = """You are the Risk Manager (The Devil's Advocate) of the Council.
Your goal is to identify ALL potential risks associated with the ticker.
You are skeptical, cautious, and focused on capital preservation.
Analyze volatility, regulatory threats, geopolitical exposure, and downside scenarios.
Consistently check if the investment aligns with the user's Prime Directive.

Prime Directive: {prime_directive}
"""

def risk_manager_node(state: AgentState):
    ticker = state["ticker"]
    prime_directive = state.get("prime_directive", "Maximize returns, minimize risk.")
    
    # 1. Search for specific risks
    risks_news = web_search(f"Risks, controversy, regulatory issues, downsides for {ticker} stock")
    
    # 2. Analyze
    messages = [
        SystemMessage(content=RISK_PROMPT.format(prime_directive=prime_directive)),
        HumanMessage(content=f"Ticker: {ticker}\n\nSearch Results for Risks:\n{risks_news}\n\nProvide a Devil's Advocate Risk Report.")
    ]
    
    response = llm.invoke(messages)
    return {"risk_report": response.content}
