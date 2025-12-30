from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import AgentState
import json

llm = ChatOpenAI(model="gpt-4o", temperature=0)

CHAIRPERSON_PROMPT = """You are the Chairperson of the Olympus Investment Council.
You have received reports from your three expert analysts (Macro, Fundamental, Technical) and a Risk Manager (Devil's Advocate).
Your job is to synthesize these reports and make a final investment decision.

PRIME DIRECTIVE: {prime_directive}

You must adhere to the Prime Directive above. If the directive says "No Crypto" and this is a crypto stock, you must REJECT it.
Construct a coherent argument based on the evidence provided.

You must output a JSON object with the following structure:
{{
    "ticker": "SYMBOL",
    "signal": "BUY" | "SELL" | "HOLD",
    "confidence": float (0-100),
    "reasoning": "Detailed summary of why...",
    "order_plan": {{
        "action": "market_buy" | "market_sell" | "none",
        "quantity_risk": "conservative" | "aggressive"
    }}
}}
Output ONLY the JSON.
"""

def chairperson_node(state: AgentState):
    reports = state["analyst_reports"]
    risk_report = state.get("risk_report", "No risk report available.")
    ticker = state["ticker"]
    prime_directive = state.get("prime_directive", "N/A")
    
    # Format reports for the chairperson
    reports_text = ""
    for role, content in reports.items():
        reports_text += f"-- {role} Report --\n{content}\n\n"
    
    reports_text += f"-- Risk Manager Report (Devil's Advocate) --\n{risk_report}\n\n"
        
    messages = [
        SystemMessage(content=CHAIRPERSON_PROMPT.format(prime_directive=prime_directive)),
        HumanMessage(content=f"Ticker: {ticker}\n\nAnalyst Reports:\n{reports_text}\n\nMake your decision.")
    ]
    
    response = llm.invoke(messages)
    
    # Basic cleaning to ensure json
    content = response.content.replace("```json", "").replace("```", "").strip()
    
    return {"final_decision": content}
