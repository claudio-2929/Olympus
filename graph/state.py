from typing import TypedDict, Annotated, List, Dict
import operator

class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    ticker: str
    prime_directive: str
    analyst_reports: Dict[str, str]
    risk_report: str
    final_decision: str
