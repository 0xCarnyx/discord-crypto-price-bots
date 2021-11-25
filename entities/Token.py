from utils.erc20_abi import ERC20_ABI
import utils.constants as constants

from abc import ABC, abstractmethod
from typing import Union, Tuple

from web3 import Web3
import requests


class Token(ABC):
    @abstractmethod
    def get_price(self, pretty_print: bool) -> Union[Tuple[str, str], Tuple[float, float]]:
        pass

    @abstractmethod
    def get_volume(self, pretty_print: bool):
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
            return f"${usd_price}"
        return usd_price

    def get_volume(self, pretty_print: bool):
        pass


class APIToken(Token):
    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_price(self, pretty_print: bool) -> Union[str, float, Tuple[str, str], Tuple[float, float]]:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.ticker}&vs_currencies=usd")
        response_data = response.json()
        usd_price = round(response_data.get(self.ticker).get("usd"), 2)
        if pretty_print:
            formatted_price = f"{constants.USD}{usd_price}"
            return formatted_price
        return usd_price

    def get_volume(self, pretty_print: bool):
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{self.ticker}?localization=false&tickers=false"
                                f"&community_data=false&developer_data=false&sparkline=false")
        response_data = response.json()
        usd_volume = round(response_data.get("market_data").get("total_volume").get("usd"), 2)
        if pretty_print:
            return f"{constants.USD}{usd_volume}"
        return usd_volume
