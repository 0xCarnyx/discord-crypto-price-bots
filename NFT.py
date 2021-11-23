from abc import ABC, abstractmethod

import requests


class NFT(ABC):
    """Represents an NFT collection.

    """
    @abstractmethod
    def get_stats(self) -> dict:
        """Retrieves dictionary with statistics about the NFT collection. Used to retrieve detailed statistics.

        :return: Statistics dictionary
        """
        pass

    @abstractmethod
    def get_floor_price(self) -> float:
        """Retrieves the current floor price in ETH for the NFT collection.

        :return: Floor price in ETH
        """
        pass

    @abstractmethod
    def get_volume(self, period: str) -> float:
        """Retrieves the volume in ETH of the NFT collection during a given time period.

        :param period: Time period
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
    def __init__(self, asset: str):
        self.asset = asset

    def get_stats(self) -> dict:
        response = requests.get(f"https://api.opensea.io/api/v1/collection/{self.asset}")
        return response.json().get("collection").get("stats")

    def get_floor_price(self) -> float:
        stats = self.get_stats()
        return stats.get("floor_price")

    def get_volume(self, period: str) -> float:
        stats = self.get_stats()
        if period == "daily":
            return stats.get("one_day_volume")
        elif period == "weekly":
            return stats.get("seven_day_volume")
        elif period == "monthly":
            return stats.get("thirty_day_volume")

    def get_num_owners(self) -> int:
        stats = self.get_stats()
        return stats.get("num_owners")
