from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from graph.state import AgentState
from tools.market_data import get_stock_prices, get_financial_info
from tools.search import web_search
import json

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- Prompts ---

MACRO_PROMPT = """You are a Macro Global Strategist. 
Your goal is to analyze the broad economic environment (inflation, interest rates, geopolitical stability) and how it impacts the specific sector of the stock in question.
Do NOT focus on the specific company financials or technical charts. Focus on the MACRO.
Use the search tool to find current relevant news.
"""

FUNDAMENTAL_PROMPT = """You are a Fundamental Equity Analyst.
Your goal is to analyze the company's financial health, valuation, and business model.
Look at P/E ratios, revenue growth, healthy balance sheet, and competitive advantage.
Use the provided financial info tool to get data.
"""

TECHNICAL_PROMPT = """You are a Technical Analyst.
Your goal is to analyze price action, trends, support/resistance levels, and momentum.
Use the stock prices tool to get historical data.
"""

# --- Agent Nodes ---

def macro_analyst_node(state: AgentState):
    ticker = state["ticker"]
    messages = [
        SystemMessage(content=MACRO_PROMPT),
        HumanMessage(content=f"Analyze the macro environment for {ticker}.")
    ]
    
    # Simple tool binding or just direct tool usage for MVP?
    # For MVP, let's use the LLM with tools bound.
    analyst_with_tools = llm.bind_tools([web_search])
    response = analyst_with_tools.invoke(messages)
    
    # Check if tool call is needed (basic ReAct loop handling is complex strictly inside one node without a prebuilt agent wrapper, 
    # but for simple single-turn or fixed-step, we can simulate. 
    # To keep it robust, let's just make the agent do a search and then synthesize).
    
    # Actually, simpler for MVP: Just get the data first, then ask LLM to analyze? 
    # Or utilize LangGraph's prebuilt agents? 
    # Let's keep it manual for control.
    
    # 1. Search for news
    news = web_search(f"Macro economic news affecting {ticker} sector")
    
    # 2. Analyze
    analysis_msg = [
        SystemMessage(content=MACRO_PROMPT),
        HumanMessage(content=f"Here is the latest news data:\n{news}\n\nAnalyze the macro outlook for {ticker}.")
    ]
    response = llm.invoke(analysis_msg)
    
    return {"analyst_reports": {"Macro Analyst": response.content}}

def fundamental_analyst_node(state: AgentState):
    ticker = state["ticker"]
    
    # 1. Get Financial Data
    data = get_financial_info(ticker)
    
    # 2. Analyze
    messages = [
        SystemMessage(content=FUNDAMENTAL_PROMPT),
        HumanMessage(content=f"Here is the financial data for {ticker}:\n{data}\n\nProvide a fundamental analysis.")
    ]
    response = llm.invoke(messages)
    return {"analyst_reports": {"Fundamental Analyst": response.content}}

def technical_analyst_node(state: AgentState):
    ticker = state["ticker"]
    
    # 1. Get Price Data
    prices = get_stock_prices(ticker, period="3mo", interval="1d")
    
    # 2. Analyze
    messages = [
        SystemMessage(content=TECHNICAL_PROMPT),
        HumanMessage(content=f"Here is the price history for {ticker}:\n{prices}\n\nProvide a technical analysis.")
    ]
    response = llm.invoke(messages)
    return {"analyst_reports": {"Technical Analyst": response.content}}
