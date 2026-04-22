from loguru import logger
from bot.client import post_order
from bot.validators import (
    validate_symbol,
    validate_quantity,
    validate_price,
    validate_stop_price
)

def place_market_order(symbol: str, side: str, quantity: float) -> dict:
    """
    Execute a Market order.
    """
    logger.info(f"Preparing MARKET {side} order for {symbol}")
    
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity
    }
    
    return post_order(params)

def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    """
    Execute a Limit order.
    """
    logger.info(f"Preparing LIMIT {side} order for {symbol} at {price}")
    
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    price = validate_price(price, "LIMIT")
    
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": quantity,
        "price": price
    }
    
    return post_order(params)

def place_stop_limit_order(symbol: str, side: str, quantity: float, price: float, stop_price: float) -> dict:
    """
    Execute a Stop-Limit order.
    Binance type is 'STOP' for a standard Stop-Limit order in Futures.
    """
    logger.info(f"Preparing STOP-LIMIT {side} order for {symbol} (Price: {price}, Stop: {stop_price})")
    
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    price = validate_price(price, "STOP")
    stop_price = validate_stop_price(stop_price, "STOP")
    
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "STOP",
        "timeInForce": "GTC",
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price
    }
    
    return post_order(params)
