"""Command-line interface for the trading bot."""

import os
import sys
import logging

import click
from dotenv import load_dotenv

from bot.client import BinanceClient, BinanceAPIError
from bot.orders import OrderManager
from bot.logging_config import setup_logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def get_api_credentials() -> tuple[str, str]:
    """Get API credentials from environment or prompt user.

    Returns:
        Tuple of (api_key, api_secret)

    Raises:
        click.ClickException: If credentials are not provided
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key:
        api_key = click.prompt("Enter BINANCE_API_KEY")
        if not api_key:
            raise click.ClickException("API key is required")

    if not api_secret:
        click.echo("Enter BINANCE_API_SECRET (input is hidden for security):")
        api_secret = click.prompt("", hide_input=True, prompt_suffix="")
        if not api_secret:
            raise click.ClickException("API secret is required")

    return api_key, api_secret


@click.group()
def cli() -> None:
    """Trading Bot CLI - Place orders on Binance Futures Testnet."""
    pass


@cli.command()
@click.option(
    "--symbol",
    required=True,
    help="Trading pair symbol (e.g., BTCUSDT)",
    type=str,
)
@click.option(
    "--side",
    required=True,
    help="Order side (BUY or SELL)",
    type=click.Choice(["BUY", "SELL"], case_sensitive=False),
)
@click.option(
    "--type",
    required=True,
    help="Order type (MARKET or LIMIT)",
    type=click.Choice(["MARKET", "LIMIT"], case_sensitive=False),
)
@click.option(
    "--quantity",
    required=True,
    help="Order quantity",
    type=float,
)
@click.option(
    "--price",
    default=None,
    help="Order price (required for LIMIT orders)",
    type=float,
)
def place_order(
    symbol: str, side: str, type: str, quantity: float, price: float
) -> None:
    """Place an order on the exchange.

    Example:
        # Market order
        python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

        # Limit order
        python cli.py place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 50000
    """
    try:
        # Get credentials
        api_key, api_secret = get_api_credentials()

        # Initialize client and manager
        client = BinanceClient(api_key, api_secret)
        manager = OrderManager(client)

        # Place order
        if type.upper() == "MARKET":
            manager.place_market_order(symbol, side, quantity)
        else:
            if price is None:
                raise click.ClickException("Price is required for LIMIT orders")
            manager.place_limit_order(symbol, side, quantity, price)

        logger.info(f"Order placed successfully")

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise click.ClickException(str(e))
    except BinanceAPIError as e:
        logger.error(f"API error: {e}")
        raise click.ClickException(f"API Error ({e.status_code}): {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise click.ClickException(f"Unexpected error: {str(e)}")


@cli.command()
def interactive() -> None:
    """Interactive menu for placing orders step by step."""
    try:
        click.clear()
        click.echo("╔════════════════════════════════════════════════════════════╗")
        click.echo("║         BINANCE FUTURES TESTNET TRADING BOT                 ║")
        click.echo("╚════════════════════════════════════════════════════════════╝\n")

        # Get credentials
        api_key, api_secret = get_api_credentials()

        # Initialize client
        client = BinanceClient(api_key, api_secret)

        # Test connection
        click.echo("\n➤ Testing API connection...")
        try:
            client.ping()
            click.secho("✓ Connection successful!", fg="green")
        except Exception as e:
            click.secho(f"✗ Connection failed: {e}", fg="red")
            return

        # Get account info
        click.echo("\n➤ Fetching account information...")
        try:
            account_info = client.get_account_info()
            click.secho("✓ Account loaded!", fg="green")
        except Exception as e:
            click.secho(f"✗ Failed to load account: {e}", fg="red")
            return

        # Initialize manager
        manager = OrderManager(client)

        # Main loop
        while True:
            click.echo("\n" + "=" * 60)
            click.echo("SELECT ORDER TYPE:")
            click.echo("=" * 60)
            order_type = click.prompt(
                "Enter order type",
                type=click.Choice(["MARKET", "LIMIT", "EXIT"], case_sensitive=False),
            )

            if order_type.upper() == "EXIT":
                click.secho("\n👋 Thank you for using Trading Bot. Goodbye!", fg="cyan")
                break

            # Get symbol
            symbol = click.prompt("Enter symbol (e.g., BTCUSDT)").upper()

            # Get side
            side = click.prompt(
                "Enter side",
                type=click.Choice(["BUY", "SELL"], case_sensitive=False),
            )

            # Get quantity
            quantity = click.prompt("Enter quantity", type=float)

            # Get price if limit order
            price = None
            if order_type.upper() == "LIMIT":
                price = click.prompt("Enter limit price", type=float)

            # Confirm before placing
            click.echo("\n" + "─" * 60)
            click.echo("ORDER DETAILS:")
            click.echo(f"  Symbol:   {symbol}")
            click.echo(f"  Side:     {side.upper()}")
            click.echo(f"  Type:     {order_type.upper()}")
            click.echo(f"  Quantity: {quantity}")
            if price is not None:
                click.echo(f"  Price:    {price}")
            click.echo("─" * 60)

            confirm = click.confirm("Place this order?", default=False)

            if not confirm:
                click.secho("✗ Order cancelled", fg="yellow")
                continue

            # Place order
            try:
                if order_type.upper() == "MARKET":
                    manager.place_market_order(symbol, side, quantity)
                else:
                    manager.place_limit_order(symbol, side, quantity, price)

                click.secho("\n✓ Order placed successfully!", fg="green")
                logger.info(f"Order placed: {symbol} {side} {quantity}")

            except ValueError as e:
                click.secho(f"\n✗ Validation error: {e}", fg="red")
                logger.error(f"Validation error: {e}")
            except BinanceAPIError as e:
                click.secho(
                    f"\n✗ API error ({e.status_code}): {e.message}",
                    fg="red",
                )
                logger.error(f"API error: {e}")
            except Exception as e:
                click.secho(f"\n✗ Error: {e}", fg="red")
                logger.error(f"Unexpected error: {e}")

    except click.ClickException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise click.ClickException(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    cli()
