from utils.erc20_abi import ERC20_ABI
import utils.constants as constants

from abc import ABC, abstractmethod
from typing import Union

from web3 import Web3
import requests


class Token(ABC):
    @abstractmethod
    def get_price(self, pretty_print: bool) -> Union[str, float]:
        pass

    @abstractmethod
    def get_trend(self, period: str):
        pass


class WETHPairedToken(Token):
    def __init__(self, lp_contract: str, token: str, w3):
        self.lp_contract = lp_contract
        self.token = token
        self.w3 = w3

    def get_price(self, pretty_print: bool) -> Union[str, float]:
        weth = Web3.toChecksumAddress(constants.WETH_ADDRESS)
        token = Web3.toChecksumAddress(self.token)
        token_weth_lp = Web3.toChecksumAddress(self.lp_contract)

        weth_erc20 = self.w3.eth.contract(address=weth, abi=ERC20_ABI)
        token_erc20 = self.w3.eth.contract(address=token, abi=ERC20_ABI)

        lp_weth_balance = weth_erc20.functions.balanceOf(token_weth_lp).call()
        lp_token_balance = token_erc20.functions.balanceOf(token_weth_lp).call()

        price_in_eth = lp_weth_balance / lp_token_balance

        current_eth_price = APIToken("ethereum").get_price(pretty_print=False)
        usd_price = round(price_in_eth * current_eth_price, 2)
        if pretty_print:
            return f"Price: ${usd_price}"
        return usd_price

    def get_trend(self, period: Union[None, str]) -> float:
        pass


class APIToken(Token):
    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_price(self, pretty_print: bool) -> Union[str, float]:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.ticker}&vs_currencies=usd")
        usd_price = round(response.json().get(self.ticker).get("usd"), 2)
        if pretty_print:
            return f"Price: ${usd_price}"
        return usd_price

    def get_trend(self, period: Union[None, str]) -> float:
        pass
