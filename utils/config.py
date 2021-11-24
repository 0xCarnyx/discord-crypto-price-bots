from pathlib import Path
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    infura_url: str
    bot_token: str

    pool_contract: str
    token_contract: str

    def __init__(self, config_file: Path):
        with config_file.open("r") as fp:
            config = yaml.safe_load(fp)
        self.infura_url = config.get("INFURA_URL")
        self.bot_token = config.get("BOT_TOKEN")

        self.pool_contract = config.get("POOL_CONTRACT")
        self.token_contract = config.get("TOKEN_CONTRACT")
