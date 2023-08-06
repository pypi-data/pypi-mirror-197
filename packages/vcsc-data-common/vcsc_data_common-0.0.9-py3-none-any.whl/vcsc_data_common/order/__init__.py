import requests
import json
import logging
import pandas as pd


class OrderException(Exception):
    pass


class Order:
    def __init__(self, paper_trading_api_end_point: str):
        self.paper_trading_api_end_point = paper_trading_api_end_point

    def place_mp_buy_order(self, username: str, portfolio_id: int, symbol: str, volume: int,):
        url = f"{self.paper_trading_api_end_point}/order/placeOrder"

        payload = json.dumps({
            "username": username,
            "symbol": symbol,
            "orderType": "MP",
            "volume": volume,
            "side": "B"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if(response.status_code != 200):
            logging.error(
                f'place_mp_buy_order: http code: {response.status_code} --> {response.text}')

            raise OrderException('place_mp_buy_order api error')

    def place_mp_sell_order(self, username: str, portfolio_id: int, symbol: str, volume: int,):
        url = f"{self.paper_trading_api_end_point}/order/placeOrder"

        payload = json.dumps({
            "username": username,
            "symbol": symbol,
            "orderType": "MP",
            "volume": volume,
            "side": "S"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if(response.status_code != 200):
            logging.error(
                f'place_mp_sell_order: http code: {response.status_code} --> {response.text}')

            raise OrderException('place_mp_sell_order api error')
