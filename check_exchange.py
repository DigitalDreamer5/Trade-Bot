"""Check exchange info and order functionality."""

import requests

print("Checking BTCUSDT on testnet.binance.vision...")
print("=" * 60)

try:
    # Get exchange info
    resp = requests.get(
        'https://testnet.binance.vision/api/v3/exchangeInfo?symbol=BTCUSDT',
        timeout=5
    )
    
    if resp.status_code == 200:
        data = resp.json()
        print("Exchange Info Retrieved:")
        print(f"  Exchange Status: {data.get('status')}")
        print(f"  Timezone: {data.get('timezone')}")
        
        if 'symbols' in data and data['symbols']:
            symbol = data['symbols'][0]
            print(f"\n  Symbol: {symbol.get('symbol')}")
            print(f"  Base Asset: {symbol.get('baseAsset')}")
            print(f"  Quote Asset: {symbol.get('quoteAsset')}")
            print(f"  Status: {symbol.get('status')}")
            print(f"  Order Types: {symbol.get('orderTypes')}")
            print(f"  Filters:")
            for f in symbol.get('filters', [])[:3]:
                print(f"    - {f.get('filterType')}: {f}")
    else:
        print(f"Failed to get exchange info")
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:500]}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Issue Summary:")
print("-" * 60)
print("✓ API credentials are VALID (account info works)")
print("✓ Account has SPOT trading ENABLED")
print("✓ Account has USDT balance")
print("✗ Order placement FAILS with signature error")
print("\nPossible causes:")
print("1. testnet.binance.vision may have order placement disabled")
print("2. Specific order parameters may be required")
print("3. API key may lack specific order permissions")
print("4. Timestamp sync issue")
