from utils.erc20_abi import ERC20_ABI
import utils.constants as constants

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Union, Tuple

from web3 import Web3
import requests


class Token(ABC):
    @abstractmethod
    def get_price(self, pretty_print: bool, get_trend: bool) -> Union[Tuple[str, str], Tuple[float, float]]:
        pass

    @abstractmethod
    def get_trend(self, current_price: float, pretty_print: bool):
        pass


class WETHPairedToken(Token):
    def __init__(self, lp_contract: str, token: str, w3):
        self.lp_contract = lp_contract
        self.token = token
        self.w3 = w3

    def get_price(self, pretty_print: bool, get_trend: bool) -> Union[str, float]:
        weth = Web3.toChecksumAddress(constants.WETH_ADDRESS)
        token = Web3.toChecksumAddress(self.token)
        token_weth_lp = Web3.toChecksumAddress(self.lp_contract)

        weth_erc20 = self.w3.eth.contract(address=weth, abi=ERC20_ABI)
        token_erc20 = self.w3.eth.contract(address=token, abi=ERC20_ABI)

        lp_weth_balance = weth_erc20.functions.balanceOf(token_weth_lp).call()
        lp_token_balance = token_erc20.functions.balanceOf(token_weth_lp).call()

        price_in_eth = lp_weth_balance / lp_token_balance

        current_eth_price = APIToken("ethereum").get_price(pretty_print=False, get_trend=False)
        usd_price = round(price_in_eth * current_eth_price, 2)
        if pretty_print:
            return f"Price: ${usd_price}"
        return usd_price

    def get_trend(self, current_price: float, pretty_print: bool) -> float:
        pass


class APIToken(Token):
    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_price(self, pretty_print: bool, get_trend: bool) -> Union[str, float, Tuple[str, str], Tuple[float, float]]:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.ticker}&vs_currencies=usd")
        response_data = response.json()
        usd_price = round(response_data.get(self.ticker).get("usd"), 2)
        change_percent = self.get_trend(usd_price, pretty_print)
        if pretty_print:
            formatted_price = f"Price: ${usd_price}"
            if get_trend:
                return formatted_price, change_percent
            return formatted_price
        if get_trend:
            return usd_price, change_percent
        return usd_price

    def get_trend(self, current_price: float, pretty_print: True) -> Union[str, Tuple[float, float]]:
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_formatted = yesterday.strftime('%d-%m-%Y')

        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{self.ticker}/history?date={yesterday_formatted}")
        response_data = response.json()
        yesterday_usd_price = response_data.get("market_data").get("current_price").get("usd")

        total_change = round(current_price - yesterday_usd_price, 2)
        percentage_change = round(((float(current_price)-yesterday_usd_price)/yesterday_usd_price)*100, 2)

        if pretty_print:
            if percentage_change > 0:
                trend_symbol = constants.PUMPING
            elif percentage_change < 0:
                trend_symbol = constants.DUMPING
            else:
                trend_symbol = constants.NEUTRAL
            return f"{trend_symbol} {str(percentage_change)}% ({str(total_change)})"
        return percentage_change, total_change
