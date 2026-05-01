# Binance Futures Testnet Trading Bot

A production-style Python trading bot for placing orders on Binance Futures Testnet. This bot provides both command-line and interactive menu interfaces for placing market and limit orders.

## Project Overview

This trading bot is built with clean architecture principles and includes:

- **BinanceClient**: Low-level API client with HMAC-SHA256 request signing
- **OrderManager**: High-level order management with validation and formatted output
- **CLI**: Click-based command-line interface for order placement
- **Interactive Menu**: Step-by-step order placement wizard
- **Comprehensive Logging**: Detailed file and console logging
- **Validation**: Robust parameter validation with clear error messages

## Features

✅ Market and limit order placement
✅ HMAC-SHA256 request signing
✅ Comprehensive error handling
✅ Full logging to file and console
✅ Interactive CLI menu
✅ Type hints and docstrings
✅ Parameter validation
✅ No hardcoded credentials
✅ Float precision protection (amounts sent as strings)

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package exports
│   ├── client.py                # BinanceClient and BinanceAPIError
│   ├── orders.py                # OrderManager for order placement
│   ├── validators.py            # Order parameter validation
│   └── logging_config.py        # Logging setup
├── cli.py                       # Click CLI application
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
└── README.md                    # This file
```

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Binance Futures Testnet account

### Step 1: Clone or Create the Project

Navigate to the project directory:

```bash
cd trading_bot
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your API credentials:
```
BINANCE_API_KEY=your_actual_api_key
BINANCE_API_SECRET=your_actual_api_secret
```

**How to get credentials:**
1. Go to https://testnet.binancefuture.com/
2. Sign up or log in
3. Navigate to Account → API Management
4. Create an API key and secret
5. Enable testnet access if required

## Usage

### Option 1: Command-Line Orders

#### Market Order Example

```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**Expected Output:**
```
============================================================
ORDER SUMMARY
============================================================
Symbol:        BTCUSDT
Side:          BUY
Type:          MARKET
Quantity:      0.01
============================================================
Placing order...

============================================================
ORDER RESPONSE
============================================================
Order ID:       1234567890
Status:         FILLED
Executed Qty:   0.01
Average Price:  43500.50
============================================================
```

#### Limit Order Example

```bash
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 45000
```

**Expected Output:**
```
============================================================
ORDER SUMMARY
============================================================
Symbol:        BTCUSDT
Side:          SELL
Type:          LIMIT
Quantity:      0.01
Price:         45000
Time in Force: GTC
============================================================
Placing order...

============================================================
ORDER RESPONSE
============================================================
Order ID:       1234567891
Status:         NEW
Executed Qty:   0.0
Average Price:  0
============================================================
```

### Option 2: Interactive Menu

Start the interactive mode:

```bash
python cli.py interactive
```

**Features:**
- Step-by-step prompts for order placement
- Real-time account information display
- Order confirmation before placement
- Color-coded output (success, error, warning)

**Walkthrough:**
```
╔════════════════════════════════════════════════════════════╗
║         BINANCE FUTURES TESTNET TRADING BOT                 ║
╚════════════════════════════════════════════════════════════╝

Enter BINANCE_API_KEY: [prompt]
Enter BINANCE_API_SECRET: [hidden prompt]

➤ Testing API connection...
✓ Connection successful!

➤ Fetching account information...
✓ Account loaded!

============================================================
SELECT ORDER TYPE:
============================================================
Enter order type [MARKET/LIMIT/EXIT]: MARKET
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side [BUY/SELL]: BUY
Enter quantity: 0.01

────────────────────────────────────────────────────────────
ORDER DETAILS:
  Symbol:   BTCUSDT
  Side:     BUY
  Type:     MARKET
  Quantity: 0.01
────────────────────────────────────────────────────────────
Place this order? [y/N]: y

✓ Order placed successfully!
```

## Logging

Logs are created in the `logs/` directory with the format: `trading_bot_YYYYMMDD.log`

**Log Levels:**
- **File**: DEBUG (all details)
- **Console**: INFO (important events only)

**Log Format:**
```
2024-05-01 14:23:45,123 | INFO     | bot.client | Placing order with params: {...}
2024-05-01 14:23:46,456 | DEBUG    | bot.validators | Order params validated: ...
```

Example log file location: `logs/trading_bot_20240501.log`

## API Methods

### BinanceClient Methods

```python
client = BinanceClient(api_key, api_secret)

# Test connectivity
client.ping()

# Get server time
server_time = client.get_server_time()

# Get account information
account_info = client.get_account_info()

# Place order (raw)
order = client.place_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity="0.01")
```

### OrderManager Methods

```python
manager = OrderManager(client)

# Place market order
order = manager.place_market_order("BTCUSDT", "BUY", 0.01)

# Place limit order
order = manager.place_limit_order("BTCUSDT", "BUY", 0.01, 45000)
```

## Error Handling

The bot handles errors gracefully at multiple levels:

### Validation Errors
```
ValueError: Symbol must be uppercase
ValueError: Side must be BUY or SELL
ValueError: Order type must be MARKET or LIMIT
ValueError: Quantity must be positive
ValueError: Price is required for LIMIT orders
```

### API Errors
```
BinanceAPIError (400): Invalid symbol
BinanceAPIError (403): Insufficient balance
BinanceAPIError (403): Invalid order price
```

### Exception Handling
All commands wrap operations in try/except blocks:
```bash
try:
    # Validation errors
except ValueError as e:
    logger.error(f"Validation error: {e}")
    raise click.ClickException(str(e))

# API errors
except BinanceAPIError as e:
    logger.error(f"API error: {e}")
    raise click.ClickException(f"API Error ({e.status_code}): {e.message}")

# Unexpected errors
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise click.ClickException(f"Unexpected error: {str(e)}")
```

## Code Quality

### Type Hints

All functions include type hints:
```python
def place_order(
    symbol: str, 
    side: str, 
    quantity: Union[int, float]
) -> Dict[str, Any]:
    """Place an order on the exchange."""
    ...
```

### Docstrings

All classes and public methods have docstrings:
```python
class OrderManager:
    """Manages order placement and tracking."""
    
    def place_market_order(
        self, symbol: str, side: str, quantity: Union[int, float]
    ) -> Dict[str, Any]:
        """Place a market order.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            ...
        """
```

### Float Precision

All amounts are converted to strings before sending to API:
```python
params = {
    "quantity": str(quantity),  # Avoid float precision issues
    "price": str(price),
}
```

## Assumptions

1. **Binance Testnet Available**: Users have access to Binance Futures Testnet at https://testnet.binancefuture.com/

2. **API Credentials**: Valid API key and secret obtained from Binance testnet account

3. **Network Connectivity**: Machine has stable internet connection to Binance API

4. **Python Version**: Python 3.8+ is installed and available

5. **No Hardcoded Credentials**: Credentials come from environment variables or interactive prompts, never hardcoded

6. **Testnet Only**: This bot is configured only for Binance Futures Testnet. Do NOT use with mainnet API URLs or credentials

7. **Order Types Supported**:
   - MARKET: Executes immediately at market price
   - LIMIT: Waits for specified price (GTC - Good Till Canceled)

8. **Base Currency**: USDT (U futures contracts)

9. **Decimal Precision**: All prices and quantities use proper decimal handling via string conversion

10. **Logging**: Logs are written to `logs/` directory in the project root

## Troubleshooting

### "API key is invalid" Error

- Verify API key and secret are correct
- Check API key is enabled on Binance testnet account
- Ensure .env file exists and has correct credentials

### "Insufficient balance" Error

- Add balance to your testnet account
- Use faucet at https://testnet.binancefuture.com/

### "Invalid symbol" Error

- Verify symbol exists on Binance (e.g., BTCUSDT, ETHUSDT)
- Use uppercase symbols

### No logs appearing

- Ensure `logs/` directory exists (auto-created)
- Check file permissions allow writing to logs directory
- Verify logging is enabled in logging_config.py

### Connection timeout

- Check internet connectivity
- Verify Binance testnet API is accessible
- Try testing with `client.ping()` first

## Development

### Running Tests

To add tests, create a `tests/` directory:

```bash
pytest tests/
```

### Adding Custom Validators

Extend `validators.py`:

```python
def validate_custom_param(value: str) -> None:
    """Custom validation logic."""
    if not is_valid(value):
        raise ValueError("Invalid value")
```

### Extending OrderManager

Add new order types:

```python
class OrderManager:
    def place_stop_loss_order(self, symbol: str, side: str, 
                             quantity: float, stop_price: float) -> Dict:
        """Place a stop-loss order."""
        ...
```

## Security Notes

🔒 **Important:**
- Never commit `.env` file with real credentials
- Use environment variables, not hardcoded values
- Rotate API keys regularly
- Use testnet credentials only for testing
- Enable IP whitelisting on API keys if possible
- Consider using read-only keys for monitoring
- Keep the bot software updated

## License

This project is provided as-is for educational and testnet trading purposes.

## Support

For issues related to:
- **Binance API**: https://binance-docs.github.io/apidocs/futures/en/
- **Click CLI**: https://click.palletsprojects.com/
- **Python Requests**: https://docs.python-requests.org/

---

**Last Updated:** May 2024
**Python Version:** 3.8+
**Status:** Production Ready
