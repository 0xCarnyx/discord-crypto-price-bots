from utils.config import Config
from entities.Token import Token, APIToken, WETHPairedToken

from pathlib import Path
import logging

from discord.ext import commands, tasks
import click
from web3 import Web3

logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s")


@click.group()
@click.version_option()
def token_bot_cli(**kwargs):
    """
    CLI entrypoint for token-bot CLI
    """


@click.command("api-token-price", help="Starts a Discord price bot for a token. Gets price from API.")
@click.option("--ticker", type=str, required=True, help="Ticker of the token on CoinGecko.")
@click.option("--refresh-rate", type=int, default=120, help="Price refresh rate in seconds.", show_default=True)
@click.option("--config", type=Path, required=True)
def api_token_price_cli(refresh_rate: int, config: Path):
    conf = Config(config)
    ticker = conf.api_id

    token = APIToken(ticker)
    token_price_bot(token, conf, refresh_rate)


@click.command("weth-pool-token-price", help="Starts a Discord price bot for a token. Gets price from LP pool.")
@click.option("--refresh-rate", type=int, default=120, help="Price refresh rate in seconds.", show_default=True)
@click.option("--config", type=Path, required=True)
def contract_token_price_cli(refresh_rate: int, config: Path):
    conf = Config(config)
    w3 = Web3(Web3.HTTPProvider(conf.infura_url))

    token = WETHPairedToken(conf.pool_contract, conf.token_contract, w3)
    token_price_bot(token, conf, refresh_rate)


def token_price_bot(token: Token, config: Config, refresh_rate: int):
    bot = commands.Bot(command_prefix="!")

    @tasks.loop(seconds=refresh_rate)
    async def update_price():
        floor_price = token.get_price(pretty_print=True)
        for guild in bot.guilds:
            me = bot.get_guild(guild.id).me
            await me.edit(nick=floor_price)

    update_price.start()
    bot.run(config.bot_token)


token_bot_cli.add_command(api_token_price_cli)
token_bot_cli.add_command(contract_token_price_cli)

if __name__ == "__main__":
    token_bot_cli()
