import NFT as NFT
import utils.constants as constants

import logging

import click
from discord.ext import commands, tasks

logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s")


@click.command("nft-floor-price-bot", help="Stats a Discord price bot for NFT collections.")
@click.option("--platform", type=click.Choice(["OpenSea"]), default="OpenSea", show_default=True)
@click.option("--asset", type=str, required=True, help="Name of the asset on the specified platform.")
@click.option("--refresh-rate", type=int, default=120, help="Price refresh rate in seconds.", show_default=True)
def nft_bot_cli(platform: str, asset: str, refresh_rate: int):
    if platform == "OpenSea":
        nft = NFT.OpenseaNFT(asset)
        main(nft, refresh_rate)


bot = commands.Bot(command_prefix="!")


def main(nft: NFT, refresh_rate: int):
    @tasks.loop(seconds=refresh_rate)
    async def update_floor_price():
        floor_price = nft.get_floor_price()

        nickname = f"{nft.get_collection().upper()}: {floor_price}{constants.ETH}"
        await bot.get_guild(123).me.edit(nick=nickname) # TODO: Determine guild id

    bot.run()


if __name__ == "__main__":
    nft_bot_cli()
