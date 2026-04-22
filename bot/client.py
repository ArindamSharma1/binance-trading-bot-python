import os
import time
import hmac
import hashlib
from urllib.parse import urlencode
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://testnet.binancefuture.com"
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")

class BinanceAPIException(Exception):
    pass

class RateLimitException(BinanceAPIException):
    pass

def _generate_signature(query_string: str) -> str:
    """
    Generate HMAC SHA256 signature for Binance API authentication.
    """
    return hmac.new(
        API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def _handle_api_error(response: httpx.Response) -> None:
    """
    Map common Binance error codes to clear, specific exceptions.
    """
    if response.status_code in (429, 418):
        logger.error("API rate limit exceeded.")
        raise RateLimitException("You have exceeded the API rate limit.")

    try:
        data = response.json()
    except Exception:
        response.raise_for_status()
        return

    code = data.get("code")
    msg = data.get("msg", "Unknown error")

    if code == -1121:
        logger.error(f"Invalid symbol: {msg}")
        raise BinanceAPIException(f"Invalid symbol provided: {msg}")
    elif code in (-2010, -2019):
        logger.error(f"Insufficient balance: {msg}")
        raise BinanceAPIException(f"Insufficient balance to place this order: {msg}")
    elif code == -1111:
        logger.error(f"Invalid price precision: {msg}")
        raise BinanceAPIException(f"Price precision is invalid for this symbol: {msg}")
    elif code and code < 0:
        logger.error(f"Binance API Error [{code}]: {msg}")
        raise BinanceAPIException(f"Binance Error: {msg} (Code: {code})")
        
    response.raise_for_status()

def post_order(params: dict) -> dict:
    """
    Send a signed POST request to the /fapi/v1/order endpoint.
    """
    if not API_KEY or not API_SECRET:
        raise ValueError("API keys not found. Please check your .env file.")

    params["timestamp"] = int(time.time() * 1000)
    query_string = urlencode(params)
    signature = _generate_signature(query_string)
    
    # Binance expects the signature in the query string or body
    # For POST, we can pass everything as query params or urlencoded data
    # Standard practice is passing the signature as part of the params
    params["signature"] = signature
    
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    
    endpoint = f"{BASE_URL}/fapi/v1/order"
    
    logger.debug(f"Sending POST request to {endpoint} with params: {params}")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(endpoint, headers=headers, params=params)
            _handle_api_error(response)
            
            result = response.json()
            logger.debug(f"API Response: {result}")
            return result
            
    except httpx.TimeoutException:
        logger.error("Network timeout while contacting Binance API.")
        raise BinanceAPIException("Network timeout: Binance API did not respond in time.")
    except httpx.RequestError as e:
        logger.error(f"Network error: {e}")
        raise BinanceAPIException(f"A network error occurred: {e}")
