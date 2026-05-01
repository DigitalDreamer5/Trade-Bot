"""Simple API diagnostic script to test credentials."""

import os
import sys
from dotenv import load_dotenv
from bot.client import BinanceClient, BinanceAPIError

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

print("=" * 60)
print("BINANCE TESTNET API DIAGNOSTIC TEST")
print("=" * 60)

if not api_key or not api_secret:
    print("❌ ERROR: API credentials not found in .env file")
    sys.exit(1)

print(f"✓ API Key found: {api_key[:20]}...")
print(f"✓ API Secret found: {api_secret[:20]}...\n")

# Initialize client
client = BinanceClient(api_key, api_secret)

# Test 1: Ping (no signature required)
print("TEST 1: Ping Server (no signature required)")
print("-" * 60)
try:
    result = client.ping()
    print("✓ SUCCESS: Server is reachable")
    print(f"  Response: {result}\n")
except Exception as e:
    print(f"❌ FAILED: {e}\n")

# Test 2: Get Server Time (no signature required)
print("TEST 2: Get Server Time (no signature required)")
print("-" * 60)
try:
    server_time = client.get_server_time()
    print(f"✓ SUCCESS: Server time: {server_time}\n")
except Exception as e:
    print(f"❌ FAILED: {e}\n")

# Test 3: Get Account Info (signature required)
print("TEST 3: Get Account Info (signature REQUIRED)")
print("-" * 60)
print("Testing if credentials are authorized...")
try:
    account = client.get_account_info()
    print("✓ SUCCESS: Account information retrieved!")
    print(f"  Balances: {len(account.get('balances', []))} assets\n")
except BinanceAPIError as e:
    print(f"❌ API ERROR ({e.status_code}): {e.message}")
    if e.status_code == 401:
        print("   → Credentials are INVALID or UNAUTHORIZED")
    elif "-1022" in str(e.message):
        print("   → Signature ERROR - API key/secret mismatch")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}\n")

print("=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
print("\nIf TEST 1 & 2 pass but TEST 3 fails:")
print("  → Your credentials are INVALID for this testnet")
print("  → Get NEW credentials from: https://testnet.binance.vision/")
print("\nIf all tests fail:")
print("  → Check internet connection")
print("  → Verify testnet.binance.vision is accessible")
