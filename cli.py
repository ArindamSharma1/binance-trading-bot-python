import sys
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Initialize logging before other imports to ensure it's set up
import bot.logging_config
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order
from bot.client import BinanceAPIException

app = typer.Typer(help="Binance Futures CLI Trading Bot")
console = Console()

def display_summary_table(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float], stop_price: Optional[float]):
    """Show a rich table summarizing the order before placing it."""
    table = Table(title="Order Summary", show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    
    if price is not None:
        table.add_row("Price", str(price))
    if stop_price is not None:
        table.add_row("Stop Price", str(stop_price))
        
    console.print(table)
    console.print("\n")

def display_success(order_response: dict):
    """Format and display a successful order response."""
    order_id = order_response.get("orderId", "N/A")
    status = order_response.get("status", "UNKNOWN")
    executed_qty = order_response.get("executedQty", "0")
    avg_price = order_response.get("avgPrice", "0")
    
    content = (
        f"[bold]Order ID:[/bold] {order_id}\n"
        f"[bold]Status:[/bold] {status}\n"
        f"[bold]Executed Qty:[/bold] {executed_qty}\n"
        f"[bold]Avg Price:[/bold] {avg_price}"
    )
    
    panel = Panel(
        content,
        title="[bold green]Order Placed Successfully[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)

def display_error(message: str):
    """Format and display an error response."""
    panel = Panel(
        f"[bold red]{message}[/bold red]",
        title="[bold red]Order Failed[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    console.print(panel)

@app.command()
def place_order(
    symbol: str = typer.Option(..., help="Trading pair, e.g., BTCUSDT"),
    side: str = typer.Option(..., help="BUY or SELL"),
    type: str = typer.Option(..., help="MARKET, LIMIT, or STOP"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, help="Limit price (required for LIMIT and STOP)"),
    stop_price: Optional[float] = typer.Option(None, help="Stop price (required for STOP)")
):
    """
    Place a new order on Binance Futures Testnet.
    """
    order_type = type.upper()
    side = side.upper()
    
    display_summary_table(symbol, side, order_type, quantity, price, stop_price)
    
    try:
        if order_type == "MARKET":
            response = place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(symbol, side, quantity, price)
        elif order_type == "STOP":
            response = place_stop_limit_order(symbol, side, quantity, price, stop_price)
        else:
            display_error(f"Unsupported order type: {order_type}")
            sys.exit(1)
            
        display_success(response)
        
    except ValueError as e:
        display_error(f"Validation Error: {str(e)}")
        sys.exit(1)
    except BinanceAPIException as e:
        display_error(str(e))
        sys.exit(1)
    except Exception as e:
        display_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    app()
