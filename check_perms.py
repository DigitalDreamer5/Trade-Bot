"""Check API key permissions."""

import os
import json
from dotenv import load_dotenv
from bot.client import BinanceClient

load_dotenv()
client = BinanceClient(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))

account = client.get_account_info()

print("Account Permissions/Restrictions:")
print("=" * 60)
if 'permissions' in account:
    print("Permissions found:")
    for perm in account['permissions']:
        print(f"  • {perm}")
else:
    print("  No explicit permissions in response")

print("\nAccount Details:")
print(f"  Maker Commission: {account.get('makerCommission')}")
print(f"  Taker Commission: {account.get('takerCommission')}")
print(f"  Buyer Commission: {account.get('buyerCommission')}")
print(f"  Seller Commission: {account.get('sellerCommission')}")
print(f"  Assets: {len(account.get('balances', []))}")
print(f"  Can Trade: {account.get('canTrade')}")
print(f"  Can Deposit: {account.get('canDeposit')}")  
print(f"  Can Withdraw: {account.get('canWithdraw')}")

print("\nFull Account Response (first 1000 chars):")
print(json.dumps(account, indent=2)[:1000])
