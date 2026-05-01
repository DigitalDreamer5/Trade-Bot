"""Binance API client for futures trading."""

import hashlib
import hmac
import logging
import time
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class BinanceAPIError(Exception):
    """Custom exception for Binance API errors."""

    def __init__(self, status_code: int, message: str) -> None:
        """Initialize BinanceAPIError.

        Args:
            status_code: HTTP status code from the API response
            message: Error message from the API or custom message
        """
        self.status_code = status_code
        self.message = message
        super().__init__(f"Binance API Error ({status_code}): {message}")


class BinanceClient:
    """Client for interacting with Binance Futures Testnet API."""

    BASE_URL = "https://testnet.binance.vision"

    def __init__(self, api_key: str, api_secret: str) -> None:
        """Initialize BinanceClient with API credentials.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sign request parameters with HMAC SHA256.

        Args:
            params: Request parameters to sign

        Returns:
            Updated params with signature
        """
        params["timestamp"] = int(time.time() * 1000)
        query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        
        logger.debug(f"Query string: {query_string}")
        logger.debug(f"Signature: {signature}")
        
        return params

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False,
    ) -> Dict[str, Any]:
        """Make HTTP request to Binance API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Request parameters
            signed: Whether the request needs signature

        Returns:
            JSON response from API

        Raises:
            BinanceAPIError: If API returns non-200 status code
        """
        params = params or {}

        if signed:
            params = self._sign_request(params)

        url = f"{self.BASE_URL}{endpoint}"

        try:
            # For Binance API, ALL requests use query string (params parameter)
            # whether GET or POST - this is required for signature validation
            response = self.session.request(method, url, params=params)
            
            logger.debug(f"{method} {endpoint} - Status: {response.status_code}, Text: {response.text[:200]}")
            
            response.raise_for_status()

            # Try to parse JSON response
            if response.text:
                return response.json()
            else:
                # Empty response is valid (e.g., for ping)
                return {}

        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP {e.response.status_code}: {e.response.text}"
            logger.error(f"API Error: {error_message}")
            raise BinanceAPIError(e.response.status_code, e.response.text) from e

        except ValueError as e:
            # JSON parsing error
            error_message = f"Invalid JSON response: {str(e)}"
            logger.error(error_message)
            raise BinanceAPIError(0, error_message) from e

        except requests.exceptions.RequestException as e:
            error_message = f"Request failed: {str(e)}"
            logger.error(error_message)
            raise BinanceAPIError(0, error_message) from e

    def ping(self) -> Dict[str, Any]:
        """Test connectivity to the API.

        Returns:
            Response from API (empty dict on success)
        """
        logger.info("Pinging Binance API")
        return self._request("GET", "/api/v3/ping")

    def get_server_time(self) -> int:
        """Get server time from Binance.

        Returns:
            Server time in milliseconds
        """
        logger.info("Fetching server time")
        response = self._request("GET", "/api/v3/time")
        return response["serverTime"]

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information including balances.

        Returns:
            Account information dictionary
        """
        logger.info("Fetching account information")
        return self._request("GET", "/api/v3/account", signed=True)

    def place_order(self, **params: Any) -> Dict[str, Any]:
        """Place an order on the exchange.

        Args:
            **params: Order parameters (symbol, side, type, quantity, price, etc.)

        Returns:
            Order response from API

        Raises:
            BinanceAPIError: If API returns error
        """
        logger.info(f"Placing order with params: {params}")
        return self._request("POST", "/api/v3/order", params=params, signed=True)
