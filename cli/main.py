from cashu.wallet.wallet import Wallet
from cashu.core.models import PostMintQuoteResponse
from cashu.core.settings import settings
from cashu.wallet.crud import store_bolt11_mint_quote, get_bolt11_mint_quote
from cashu.core.base import MintQuote
from cashu.core.base import Unit
from cashu.core.helpers import sum_proofs
import click
import asyncio
import httpx
from urllib.parse import urljoin  # Use urljoin for URLs

settings.tor = False  # Disable Tor for this example

WALLET_DIR = "data/wallet"


@click.group()
def cli():
    pass


@click.command()
@click.option("--url", required=True, help="Mint URL")
@click.option("--id", default="default", help="The mint quote id")
@click.option("--amount", help="Amount to mint", type=int)
def mint(url: str, id: str, amount: int):
    asyncio.run(mint_async(url, id, amount))


async def mint_async(url: str, id: str, amount: int):
    w = await Wallet.with_db(url, WALLET_DIR)  # Provide DB name
    await w.load_mint()
    async with httpx.AsyncClient() as client:
        quote_local = await get_bolt11_mint_quote(w.db, id)
        if not quote_local:
            resp = await client.get(urljoin(url, f"v1/mint/quote/bolt11/{id}"))
            quote_resp = PostMintQuoteResponse.parse_obj(resp.json())
            quote_local = MintQuote.from_resp_wallet(
                quote_resp, url, amount, Unit.sat.name
            )
            await store_bolt11_mint_quote(w.db, quote_local)
        quote = quote_local
        proofs = await w.mint(amount, quote.quote)
        print(f"Minted {sum_proofs(proofs)} sats")
        print(f"Check with: CASHU_DIR=data cashu -h {url} balance")


@click.command()
@click.option("--url", required=True, help="Mint URL")
@click.option("--amount", help="Amount to mint", type=int)
def mint_quote(url: str, amount: int):
    asyncio.run(mint_quote_async(url, amount))


async def mint_quote_async(url: str, amount: int):
    w = await Wallet.with_db(url, WALLET_DIR)  # Provide DB name
    await w.load_mint()
    quote = await w.request_mint(amount)
    print(quote)


# Register commands to the CLI group
cli.add_command(mint)
cli.add_command(mint_quote)

if __name__ == "__main__":
    cli()
