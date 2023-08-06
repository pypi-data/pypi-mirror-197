# Bybit V5 Client

[![Test](https://github.com/cmpz-dev/bybit-v5-client/actions/workflows/test.yml/badge.svg)](https://github.com/cmpz-dev/bybit-v5-client/actions/workflows/test.yml)
[![Lint](https://github.com/cmpz-dev/bybit-v5-client/actions/workflows/lint.yml/badge.svg)](https://github.com/cmpz-dev/bybit-v5-client/actions/workflows/lint.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/cmpz-dev/bybit-v5-client/branch/main/graph/badge.svg?token=g59uAwRsFw)](https://codecov.io/gh/cmpz-dev/bybit-v5-client)

## Install
```shell
pip install bybit-v5-client
```

## Usage
```python
from bybit_v5_client import BybitClient

client = BybitClient(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
payload = {
    "category": "spot",
    "symbol": "BTCUSDT",
    "side": "Buy",
    "orderType": "Market",
    "qty": "0.1",
}
res = client.request(endpoint="/v5/order/create", method="POST", payload=payload)
```
