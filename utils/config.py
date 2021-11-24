from pathlib import Path
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    infura_url: str
    bot_token: str

    def __init__(self, config_file: Path):
        with config_file.open("r") as fp:
            config = yaml.safe_load(fp)
        self.infura_url = config.get("INFURA_URL")
        self.bot_token = config.get("BOT_TOKEN")
