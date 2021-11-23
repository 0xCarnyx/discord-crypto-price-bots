import requests


class NFT:
    def __init__(self, asset: str):
        self.asset = asset

    def get_stats(self) -> dict:
        response = requests.get(f"https://api.opensea.io/api/v1/collection/{self.asset}")
        return response.json().get("stats")

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
