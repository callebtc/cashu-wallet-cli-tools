Small CLI tool for manual Cashu operations

Clone this repository and install with `poetry install`. See the nutshell repository for more detailed instructions on how to install Python and Poetry: https://github.com/cashubtc/nutshell

Create a new mint quote:

```sh
poetry run cli mint --url https://testnut.cashu.space --amount <amount>
```

Mint a quote (you need to know its ID and the amount, only works with "sat")

```sh
poetry run cli mint --url https://testnut.cashu.space --id <id> --amount <amount>
```

If you have nutshell installed on your machine (`pip install cashu`), you can use it to interact with the wallet database file from this CLI tool:

```
CASHU_DIR=data cashu -h https://testnut.cashu.space balance
```