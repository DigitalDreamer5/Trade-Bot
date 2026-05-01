"""Order management for trading bot."""

import logging
from typing import Any, Dict, Union

from bot.client import BinanceClient, BinanceAPIError
from bot.validators import validate_order_params

logger = logging.getLogger(__name__)


class OrderManager:
    """Manages order placement and tracking."""

    def __init__(self, client: BinanceClient) -> None:
        """Initialize OrderManager with a Binance client.

        Args:
            client: BinanceClient instance for API communication
        """
        self.client = client

    def place_market_order(
        self, symbol: str, side: str, quantity: Union[int, float]
    ) -> Dict[str, Any]:
        """Place a market order.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity

        Returns:
            Order response from API

        Raises:
            ValueError: If parameters are invalid
            BinanceAPIError: If API call fails
        """
        # Validate parameters
        validate_order_params(symbol, side, "MARKET", quantity)

        # Prepare order parameters
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "MARKET",
            "quantity": str(quantity),  # Send as string to avoid float precision issues
            "recvWindow": 5000,  # Required for API signature
            "newOrderRespType": "RESULT",  # Response type
        }

        # Print order summary
        self._print_order_summary(params)

        try:
            # Place order
            response = self.client.place_order(**params)

            # Print formatted response
            self._print_order_response(response)

            # Log the order
            logger.info(
                f"Market order placed successfully: {symbol} {side} {quantity}"
            )

            return response

        except BinanceAPIError as e:
            logger.error(f"Failed to place market order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {e}")
            raise

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: Union[int, float],
        price: Union[int, float],
    ) -> Dict[str, Any]:
        """Place a limit order.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
            price: Order limit price

        Returns:
            Order response from API

        Raises:
            ValueError: If parameters are invalid
            BinanceAPIError: If API call fails
        """
        # Validate parameters
        validate_order_params(symbol, side, "LIMIT", quantity, price)

        # Prepare order parameters
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "LIMIT",
            "timeInForce": "GTC",  # Good-Til-Canceled
            "quantity": str(quantity),  # Send as string to avoid float precision issues
            "price": str(price),  # Send as string to avoid float precision issues
            "recvWindow": 5000,  # Required for API signature
        }

        # Print order summary
        self._print_order_summary(params)

        try:
            # Place order
            response = self.client.place_order(**params)

            # Print formatted response
            self._print_order_response(response)

            # Log the order
            logger.info(
                f"Limit order placed successfully: {symbol} {side} {quantity} @ {price}"
            )

            return response

        except BinanceAPIError as e:
            logger.error(f"Failed to place limit order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {e}")
            raise

    @staticmethod
    def _print_order_summary(params: Dict[str, Any]) -> None:
        """Print formatted order summary before placing.

        Args:
            params: Order parameters
        """
        print("\n" + "=" * 60)
        print("ORDER SUMMARY")
        print("=" * 60)
        print(f"Symbol:        {params.get('symbol', 'N/A')}")
        print(f"Side:          {params.get('side', 'N/A')}")
        print(f"Type:          {params.get('type', 'N/A')}")
        print(f"Quantity:      {params.get('quantity', 'N/A')}")
        if "price" in params:
            print(f"Price:         {params.get('price', 'N/A')}")
        if "timeInForce" in params:
            print(f"Time in Force: {params.get('timeInForce', 'N/A')}")
        print("=" * 60)
        print("Placing order...")

    @staticmethod
    def _print_order_response(response: Dict[str, Any]) -> None:
        """Print formatted order response after placement.

        Args:
            response: Order response from API
        """
        print("\n" + "=" * 60)
        print("ORDER RESPONSE")
        print("=" * 60)
        print(f"Order ID:       {response.get('orderId', 'N/A')}")
        print(f"Status:         {response.get('status', 'N/A')}")
        print(f"Executed Qty:   {response.get('executedQty', 'N/A')}")
        print(f"Average Price:  {response.get('avgPrice', 'N/A')}")
        print("=" * 60 + "\n")
