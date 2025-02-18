Small CLI tool for manual Cashu operations

Create a new mint quote:

```sh
poetry run cli mint --url https://testnut.cashu.space --amount <amount>
```

Mint a quote (you need to know its ID and the amount, only works with "sat")

```sh
poetry run cli mint --url https://testnut.cashu.space --id <id> --amount <amount>
```
