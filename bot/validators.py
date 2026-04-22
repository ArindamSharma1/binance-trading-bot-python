def validate_symbol(symbol: str) -> str:
    """
    Ensure the symbol is formatted correctly for USDT-M Futures.
    Most basic check is that it's uppercase and ends with USDT.
    """
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        raise ValueError(f"Invalid symbol format: {symbol}. Expected a USDT pair (e.g., BTCUSDT).")
    return symbol

def validate_quantity(quantity: float) -> float:
    """
    Validate that the quantity is positive.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(price: float | None, order_type: str) -> float | None:
    """
    Validate price requirements based on the order type.
    """
    if order_type in ("LIMIT", "STOP") and (price is None or price <= 0):
        raise ValueError(f"A valid positive price is required for {order_type} orders.")
    return price

def validate_stop_price(stop_price: float | None, order_type: str) -> float | None:
    """
    Validate stop_price requirements for STOP orders.
    """
    if order_type == "STOP" and (stop_price is None or stop_price <= 0):
        raise ValueError("A valid positive stop_price is required for STOP orders.")
    return stop_price
