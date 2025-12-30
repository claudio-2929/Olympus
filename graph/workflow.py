from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.analysts import macro_analyst_node, fundamental_analyst_node, technical_analyst_node
from agents.chairperson import chairperson_node

from agents.risk_manager import risk_manager_node

def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("macro_analyst", macro_analyst_node)
    workflow.add_node("fundamental_analyst", fundamental_analyst_node)
    workflow.add_node("technical_analyst", technical_analyst_node)
    workflow.add_node("risk_manager", risk_manager_node)
    workflow.add_node("chairperson", chairperson_node)
    
    # Add edges
    # Sequential MVP flow:
    workflow.set_entry_point("macro_analyst")
    workflow.add_edge("macro_analyst", "fundamental_analyst")
    workflow.add_edge("fundamental_analyst", "technical_analyst")
    workflow.add_edge("technical_analyst", "risk_manager")
    workflow.add_edge("risk_manager", "chairperson")
    workflow.add_edge("chairperson", END)
    
    return workflow.compile()
