"""Order parameter validation functions."""

import logging
from typing import Union

logger = logging.getLogger(__name__)


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Union[int, float],
    price: Union[int, float, None] = None,
) -> None:
    """Validate order parameters before placing an order.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        order_type: Order type (MARKET or LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT orders)

    Raises:
        ValueError: If any parameter is invalid
    """
    # Validate symbol
    if not symbol or not isinstance(symbol, str):
        error_msg = "Symbol must be a non-empty string"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if symbol != symbol.upper():
        error_msg = "Symbol must be uppercase"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validate side
    side = side.upper()
    if side not in ("BUY", "SELL"):
        error_msg = "Side must be BUY or SELL"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validate order type
    order_type = order_type.upper()
    if order_type not in ("MARKET", "LIMIT"):
        error_msg = "Order type must be MARKET or LIMIT"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validate quantity
    try:
        qty_float = float(quantity)
        if qty_float <= 0:
            error_msg = "Quantity must be positive"
            logger.error(error_msg)
            raise ValueError(error_msg)
    except (ValueError, TypeError) as e:
        error_msg = f"Quantity must be a positive number: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e

    # Validate price for LIMIT orders
    if order_type == "LIMIT":
        if price is None:
            error_msg = "Price is required for LIMIT orders"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            price_float = float(price)
            if price_float <= 0:
                error_msg = "Price must be positive"
                logger.error(error_msg)
                raise ValueError(error_msg)
        except (ValueError, TypeError) as e:
            error_msg = f"Price must be a positive number: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    logger.debug(
        f"Order params validated: {symbol} {side} {order_type} qty={quantity} price={price}"
    )
