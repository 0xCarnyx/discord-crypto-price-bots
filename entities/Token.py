from utils.erc20_abi import ERC20_ABI
from utils.config import Config

from abc import ABC, abstractmethod
from typing import Union

from web3 import Web3
import requests


w3 = Web3(Web3.HTTPProvider(Config.infura_url))


class Token(ABC):
    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_trend(self, period: str):
        pass


class WETHPairedToken(Token):
    def __init__(self, token: str, lp_contract: str):
        self.lp_contract = lp_contract
        self.token = token

    def get_price(self) -> float:
        weth = Web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
        token = Web3.toChecksumAddress(self.token)
        token_weth_lp = Web3.toChecksumAddress(self.lp_contract)

        weth_erc20 = w3.eth.contract(address=weth, abi=ERC20_ABI)
        token_erc20 = w3.eth.contract(address=token, abi=ERC20_ABI)

        lp_weth_balance = weth_erc20.functions.balanceOf(token_weth_lp).call()
        lp_token_balance = token_erc20.functions.balanceOf(token_weth_lp).call()

        price_in_eth = lp_weth_balance / lp_token_balance

        current_eth_price = APIToken("eth").get_price()

        return price_in_eth * current_eth_price

    def get_trend(self, period: Union[None, str]) -> float:
        pass


class APIToken(Token):
    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_price(self) -> float:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.ticker}&vs_currencies=usd")
        return response.json().get(self.ticker).get("usd")

    def get_trend(self, period: Union[None, str]) -> float:
        pass
