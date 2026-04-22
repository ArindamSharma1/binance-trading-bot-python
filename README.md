# Binance Futures CLI Bot

A CLI tool to place Market, Limit, and Stop-Limit orders on the Binance Futures Testnet (USDT-M). 

I used `httpx` instead of `python-binance` to keep dependencies light and retain direct control over async-ready HTTP calls and error handling.

## What it does

- Places MARKET, LIMIT, and STOP (Stop-Limit) orders via the Binance REST API.
- Signs requests using HMAC SHA256.
- Validates basic inputs before making network calls.
- Logs minimal output to the console and verbose debug output to a rotating file.

## Setup

1. Clone or download the code.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`.
4. Add your Binance Testnet API key and secret to the `.env` file.

## How to run

Use the CLI to place orders. Here are some examples.

**Market Order:**
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit Order:**
```bash
python cli.py place-order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 3000
```

**Stop-Limit Order (Bonus):**
```bash
python cli.py place-order --symbol BTCUSDT --side SELL --type STOP --quantity 0.001 --price 84000 --stop-price 84500
```

## Example Output & Logs

When you run a command, you get a clean summary table and a success/failure panel in the console.

**Console Output (Market Order):**
```
Order Summary
┏━━━━━━━━━━━┳━━━━━━━━━┓
┃ Parameter ┃ Value   ┃
┡━━━━━━━━━━━╇━━━━━━━━━┩
│ Symbol    │ BTCUSDT │
│ Side      │ BUY     │
│ Type      │ MARKET  │
│ Quantity  │ 0.001   │
└───────────┴─────────┘

╭──────────────── Order Placed Successfully ────────────────╮
│ Order ID: 4569123841                                      │
│ Status: NEW                                               │
│ Executed Qty: 0                                           │
│ Avg Price: 0.00                                           │
╰───────────────────────────────────────────────────────────╯
```

**File Logs (`logs/bot_YYYY-MM-DD.log`):**
```
2026-04-22 10:15:30.123 | INFO     | bot.orders:place_market_order:12 - Preparing MARKET BUY order for BTCUSDT
2026-04-22 10:15:30.125 | DEBUG    | bot.client:post_order:64 - Sending POST request to https://testnet.binancefuture.com/fapi/v1/order with params: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001, 'timestamp': 1713780930125, 'signature': 'a1b2c3d4e5f6...'}
2026-04-22 10:15:30.450 | DEBUG    | bot.client:post_order:70 - API Response: {'orderId': 4569123841, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-xc7...'}
```

**Limit Order Log Example:**
```
2026-04-22 10:20:15.001 | INFO     | bot.orders:place_limit_order:28 - Preparing LIMIT SELL order for ETHUSDT at 3000.0
2026-04-22 10:20:15.003 | DEBUG    | bot.client:post_order:64 - Sending POST request to https://testnet.binancefuture.com/fapi/v1/order with params: {'symbol': 'ETHUSDT', 'side': 'SELL', 'type': 'LIMIT', 'timeInForce': 'GTC', 'quantity': 0.05, 'price': 3000.0, 'timestamp': 1713781215003, 'signature': 'f9e8d7c6b5a4...'}
2026-04-22 10:20:15.300 | DEBUG    | bot.client:post_order:70 - API Response: {'orderId': 9876543210, 'symbol': 'ETHUSDT', 'status': 'NEW', 'clientOrderId': 'x-xc7...', 'price': '3000.00'}
```

## Assumptions made
- The user is trading USDT-M futures on the testnet.
- Time in force is hardcoded to GTC for limit and stop orders.
- The system clock is synced correctly (Binance is strict about timestamps).

## Known limitations
- Only supports basic order types. Take Profit and Trailing Stops are not implemented.
- Does not check current market price before placing orders.
- Price and quantity precision are not dynamically fetched from exchange info. You must provide valid float values that respect the tick size.
- Hardcoded to the testnet URL.
