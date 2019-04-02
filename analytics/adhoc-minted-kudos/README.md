### minted kudos analysis

1. crendentials have been hardcoded into two methods of the script, instructions provided below to ensure you have the credentials necessary to access etherscan and gdax
2. `cd ~`
3. `mkdir .creds`
4. `touch etherscan_creds.json`

```
{
    "key": "YOUR_KEY_HERE",
    "address": "PUBLIC_ADDRESS_WALLET"
}
```
5. `touch gdax_api_creds.json`

```
{
    "key": "YOUR_KEY_HERE",
    "passphrase": "PUBLIC_ADDRESS_WALLET",
    "secret": "YOUR_SECRET_HERE"
}
```

6. `python minted_kudos_analysis.py`
7. returns minted kudos revenue of all time and month over month

