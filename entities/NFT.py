import utils.constants as constants

from abc import ABC, abstractmethod
from typing import Union

import requests


class NFT(ABC):
    """Represents an NFT collection.

    """

    @abstractmethod
    def get_collection(self) -> str:
        """Returns the classifier of the NFT collection
        """
        pass

    @abstractmethod
    def get_stats(self) -> dict:
        """Retrieves dictionary with statistics about the NFT collection. Used to retrieve detailed statistics.

        :return: Statistics dictionary
        """
        pass

    @abstractmethod
    def get_floor_price(self, pretty_print: bool) -> float:
        """Retrieves the current floor price in ETH for the NFT collection.

        :param pretty_print: Whether to return the raw value of a formatted string
        :return: Floor price in ETH as float or pretty printed string
        """
        pass

    @abstractmethod
    def get_volume(self, period: str, pretty_print: bool) -> float:
        """Retrieves the volume in ETH of the NFT collection during a given time period.

        :param period: Time period
        :param pretty_print: Whether to return the raw value of a formatted string
        :return: Volume in ETH during the given time period
        """
        pass

    @abstractmethod
    def get_num_owners(self) -> float:
        """Return the number of addresses which own at least one NFT of the NFT collection.

        :return: Number of addresses which possess at least one NFT of the NFt collection
        """
        pass


class OpenseaNFT(NFT):
    def __init__(self, collection: str):
        self.collection = collection

    def get_collection(self) -> str:
        return self.collection

    def get_stats(self) -> dict:
        response = requests.get(f"https://api.opensea.io/api/v1/collection/{self.collection}")
        return response.json().get("collection").get("stats")

    def get_floor_price(self, pretty_print: bool) -> Union[str, float]:
        stats = self.get_stats()
        if pretty_print:
            return f"Floor Price: {stats.get('floor_price')}{constants.ETH_SYMBOL}"
        return stats.get("floor_price")

    def get_volume(self, period: str, pretty_print: bool) -> Union[None, float]:
        stats = self.get_stats()
        if period == "daily":
            volume = stats.get("one_day_volume")
        elif period == "weekly":
            volume = stats.get("seven_day_volume")
        elif period == "monthly":
            volume = stats.get("thirty_day_volume")
        else:
            return None

        if pretty_print:
            f"{period.capitalize()} Volume: {volume}{constants.ETH_SYMBOL}"
        return volume

    def get_num_owners(self) -> int:
        stats = self.get_stats()
        return stats.get("num_owners")
