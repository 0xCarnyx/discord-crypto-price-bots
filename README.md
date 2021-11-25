# discord-crypto-price-bots
Discord bots for showing various metrics (price, volume, ...) for NFTs and crypto tokens. Originally designed for the LEVX DAO discord.

## Available bots
* [$LEVX price](https://discord.com/api/oauth2/authorize?client_id=912733687647469590&permissions=67108864&scope=bot)
* [Sharkpunks floor price](https://discord.com/api/oauth2/authorize?client_id=913133731185831936&permissions=67108864&scope=bot)
* [Sharkpunks weekly volume](https://discord.com/api/oauth2/authorize?client_id=913382428880568331&permissions=67108864&scope=bot)
* [$MAID price](https://discord.com/api/oauth2/authorize?client_id=913383753592750100&permissions=67108864&scope=bot)
* [$MAID volume](https://discord.com/api/oauth2/authorize?client_id=913421371466457099&permissions=67108864&scope=bot)
## Self hosting
1) Install requirements (using a virtual environment is recommended)
```
pip install -r requirements.txt
```
2) Configure a bot specific `.yaml` config file to your likings (use of one the templates provided under `/config-templates`)
3) Run the bot (see below for usage)
## Usage
### nft-bot
```
Usage: nft_bot.py [OPTIONS] COMMAND [ARGS]...

  CLI entrypoint for nft-bot CLI

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  floor-price  Stats a Discord price bot for NFT collections.
  volume       Stats a Discord price bot for NFT collections.
```
#### nft-bot (floor-price)
``` 
Usage: nft_bot.py floor-price [OPTIONS]

  Stats a Discord price bot for NFT collections.

Options:
  --platform [OpenSea]    [default: OpenSea]
  --refresh-rate INTEGER  Price refresh rate in seconds.  [default: 120]
  --config PATH           [required]
  --help                  Show this message and exit.
```
#### nft-bot (volume)
``` 
Usage: nft_bot.py volume [OPTIONS]

  Stats a Discord price bot for NFT collections.

Options:
  --platform [opensea]            [default: opensea]
  --period [daily|weekly|monthly]
  --refresh-rate INTEGER          Price refresh rate in seconds.  [default:
                                  60]
  --config PATH                   [required]
  --help                          Show this message and exit.
```
### token-bot
``` 
Usage: token_bot.py [OPTIONS] COMMAND [ARGS]...

  CLI entrypoint for token-bot CLI

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  api-token-price        Starts a Discord price bot for a token.
  api-token-volume       Starts a Discord volume bot for a token.
  weth-pool-token-price  Starts a Discord price bot for a token.
```
#### token-bot (api-token-price)
``` 
Usage: token_bot.py api-token-price [OPTIONS]

  Starts a Discord price bot for a token. Gets price from API.

Options:
  --refresh-rate INTEGER  Price refresh rate in seconds.  [default: 120]
  --config PATH           [required]
  --help                  Show this message and exit.
```
#### token-bot (api-token-volume)
``` 
Usage: token_bot.py api-token-volume [OPTIONS]

  Starts a Discord volume bot for a token. Gets volume from API.

Options:
  --refresh-rate INTEGER  Volume refresh rate in seconds.  [default: 120]
  --config PATH           [required]
  --help                  Show this message and exit.
```
##### token-bot (weth-pool-token-price)
``` 
Usage: token_bot.py weth-pool-token-price [OPTIONS]

  Starts a Discord price bot for a token. Gets price from LP pool.

Options:
  --refresh-rate INTEGER  Price refresh rate in seconds.  [default: 120]
  --config PATH           [required]
  --help                  Show this message and exit.
```