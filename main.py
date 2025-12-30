import os
import sys
from dotenv import load_dotenv
from graph.workflow import create_graph

# Load environment variables
load_dotenv()

def main():
    print("Welcome to Olympus - AI Investment Council")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env")
        return
        
    ticker = input("Enter ticker symbol to analyze (e.g., AAPL): ").strip().upper()
    if not ticker:
        print("Invalid ticker.")
        return

    prime_directive = input("Enter Prime Directive (e.g. 'Maximize growth, high risk ok'): ").strip()
    if not prime_directive:
        prime_directive = "Maximize returns, minimize risk." # Default

    print(f"\n--- Convening the Council for {ticker} ---\n")
    print(f"Prime Directive: {prime_directive}\n")
    
    app = create_graph()
    initial_state = {
        "messages": [],
        "ticker": ticker,
        "prime_directive": prime_directive,
        "analyst_reports": {},
        "risk_report": "",
        "final_decision": ""
    }
    
    # Stream the updates
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"Finished: {key}")
            # Optional: print partial results
            # if "analyst_reports" in value:
            #     print(value["analyst_reports"])
    
    print("\n--- Final Decision ---\n")
    # Get the final state (doing it via invoke for clean final return if stream is just steps)
    # Or just capture the last output.
    # Let's just re-invoke (expensive) or just trust the stream output?
    # Stream returns the update.
    # Let's invoke once for the final result if stream debugging is not priority vs clean output.
    
    result = app.invoke(initial_state)
    decision = result.get("final_decision")
    print(decision)

if __name__ == "__main__":
    main()
