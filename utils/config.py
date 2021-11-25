from pathlib import Path
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    infura_url: str
    bot_token: str

    token_name: str

    pool_contract: str
    token_contract: str

    api_id: str

    collection: str

    def __init__(self, config_file: Path):
        with config_file.open("r") as fp:
            config = yaml.safe_load(fp)
        self.infura_url = config.get("INFURA_URL")
        self.bot_token = config.get("BOT_TOKEN")

        self.token_name = config.get("TOKEN_NAME")

        self.pool_contract = config.get("POOL_CONTRACT")
        self.token_contract = config.get("TOKEN_CONTRACT")

        self.api_id = config.get("API_ID")

        self.collection = config.get("COLLECTION_NAME")
