import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

def execute_order(tier_decision: dict):
    """
    Executes a market order based on the Chairperson's decision.
    Args:
        tier_decision: JSON dict containing 'ticker', 'signal', 'order_plan'.
    """
    api_key = os.getenv("APCA_API_KEY_ID")
    secret_key = os.getenv("APCA_API_SECRET_KEY")
    paper_url = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")
    
    if not api_key or not secret_key:
        return "Alpaca API keys not found. Skipping execution."

    client = TradingClient(api_key, secret_key, paper=True) # Ensure paper=True or handling via URL? 
    # alpaca-py handles 'paper' arg. If base_url is custom, likely needed. 
    # But simplicity: explicit keys.
    
    ticker = tier_decision.get("ticker")
    signal = tier_decision.get("signal", "HOLD").upper()
    order_plan = tier_decision.get("order_plan", {})
    action = order_plan.get("action", "none").lower()
    
    if signal == "HOLD" or action == "none":
        return "Decision is HOLD. No order executed."
    
    qty = 1 # Logic for quantity sizing can be complex. For MVP fixed qty or $ amount.
    money_to_spend = 1000 # Default simulated amount
    
    # We can use notional or qty. Let's use notional if possible, else qty.
    # Alpaca support fractional.
    
    side = OrderSide.BUY if signal == "BUY" else OrderSide.SELL
    
    try:
        # Check if we own it for SELL
        if side == OrderSide.SELL:
             # Very basic check
             try:
                 pos = client.get_open_position(ticker)
                 qty = float(pos.qty) # Sell all?
             except:
                 return f"Cannot SELL {ticker}: No position found."

        # Safety: MVP only buys 1 simulation unit or fixed amount logic 
        # But let's stick to user request: "MVP"
        
        req = MarketOrderRequest(
            symbol=ticker,
            qty=qty if side == OrderSide.SELL else None,
            notional=1000 if side == OrderSide.BUY else None, # Buy $1000 worth
            side=side,
            time_in_force=TimeInForce.DAY
        )
        
        order = client.submit_order(order_request=req)
        return f"Order Executed! ID: {order.id}, Status: {order.status}, Side: {side}, Ticker: {ticker}"
        
    except Exception as e:
        return f"Order Execution Failed: {e}"
