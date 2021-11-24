import NFT as NFT
import utils.constants as constants
from utils.config import Config

import logging
from pathlib import Path

import click
from discord.ext import commands, tasks

logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s")


@click.group()
@click.version_option()
def nft_bot_cli(**kwargs):
    """
    CLI entrypoint for nft-bot CLI
    """


@click.command("floor-price", help="Stats a Discord price bot for NFT collections.")
@click.option("--platform", type=click.Choice(["OpenSea"]), default="OpenSea", show_default=True)
@click.option("--asset", type=str, required=True, help="Name of the asset on the specified platform.")
@click.option("--refresh-rate", type=int, default=120, help="Price refresh rate in seconds.", show_default=True)
@click.option("--config", type=Path, required=True)
def floor_price_cli(platform: str, asset: str, refresh_rate: int, config: Path):
    conf = Config(config)

    if platform == "OpenSea":
        nft = NFT.OpenseaNFT(asset)
        floor_price_bot(nft, conf, refresh_rate)


def floor_price_bot(nft: NFT, config: Config, refresh_rate: int):
    bot = commands.Bot(command_prefix="!")

    @tasks.loop(seconds=refresh_rate)
    async def update_floor_price():
        floor_price = nft.get_floor_price()
        for guild in bot.guilds:
            await bot.get_guild(guild.id).me.edit(nick=floor_price)

    update_floor_price.start()
    bot.run(config.bot_token)


@click.command("volume", help="Stats a Discord price bot for NFT collections.")
@click.option("--platform", type=click.Choice(["opensea"]), default="opensea", show_default=True)
@click.option("--asset", type=str, required=True, help="Name of the asset on the specified platform.")
@click.option("--period", type=click.Choice(["daily", "weekly", "monthly"]), default="daily")
@click.option("--refresh-rate", type=int, default=120, help="Price refresh rate in seconds.", show_default=True)
@click.option("--config", type=Path, required=True)
def volume_cli(platform: str, asset: str, period: str, refresh_rate: int, config: Path):
    conf = Config(config)

    if platform == "opensea":
        nft = NFT.OpenseaNFT(asset)
        volume_bot(nft, conf, period, refresh_rate)


def volume_bot(nft: NFT, config: Config, period: str, refresh_rate: int):
    bot = commands.Bot(command_prefix="!")

    @tasks.loop(seconds=refresh_rate)
    async def update_volume():
        volume = nft.get_volume(period, pretty_print=True)
        for guild in bot.guilds:
            await bot.get_guild(guild).me.edit(nick=volume)

    update_volume.start()
    bot.run(config.bot_token)


nft_bot_cli.add_command(floor_price_cli)


if __name__ == "__main__":
    nft_bot_cli()
