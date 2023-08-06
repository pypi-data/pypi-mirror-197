import hashlib
import hmac
import json
import logging
import time
from typing import Literal
from urllib.parse import urlencode

import requests
from requests import Response, Session


class BybitClient:
    _url: str
    _recv_window: str
    _time_stamp: str
    _api_key: str
    _api_secret: str
    _log: bool

    def __init__(
        self,
        test_net: bool = False,
        api_key: str = None,
        api_secret: str = None,
        log: bool = True,
    ):
        if sum(bool(x) for x in [api_key, api_secret]) == 1:
            raise Exception("Both api_key and api_secret are required")
        self._url = (
            "https://api-testnet.bybit.com" if test_net else "https://api.bybit.com"
        )
        self._recv_window = str(5000)
        self._time_stamp = str(int(time.time() * 10**3))
        self._api_key = api_key
        self._api_secret = api_secret
        self._log = log

    def _gen_signature(self, payload: str):
        param_str = str(self._time_stamp) + self._api_key + self._recv_window + payload
        hash = hmac.new(
            bytes(self._api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256
        )
        signature = hash.hexdigest()
        return signature

    @staticmethod
    def _gen_data(method: Literal["GET", "POST"], payload: dict) -> str:
        if method == "POST":
            payload = {k: str(v) for (k, v) in payload.items()}
            return json.dumps(payload).replace(" ", "")
        else:
            return urlencode(payload)

    def request(
        self, endpoint: str, method: Literal["GET", "POST"], payload: dict
    ) -> dict:
        headers: dict = {}
        str_data: str = self._gen_data(method, payload)
        if self._api_key is not None:
            assert self._api_secret is not None
            headers["X-BAPI-SIGN"] = self._gen_signature(str_data)
            headers["X-BAPI-API-KEY"] = self._api_key
            headers["X-BAPI-TIMESTAMP"] = self._time_stamp
            headers["X-BAPI-RECV-WINDOW"] = self._recv_window

        if method == "POST":
            assert self._api_key is not None and self._api_secret is not None
            headers["Content-Type"] = "application/json"
            param = {
                "method": method,
                "url": self._url + endpoint,
                "data": str_data,
                "headers": headers,
            }
        elif method == "GET":
            param = {
                "method": method,
                "url": self._url + endpoint + "?" + str_data,
                "headers": headers,
            }
        else:
            raise Exception(f"{method} is unsupported HTTP method")

        if self._log:
            base_url: str = param["url"][: param["url"].find("?")]
            logging.info({"method": param["method"], "url": base_url})
        try:
            result: Response = Session().request(**param)
            result.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return result.json()
