## Summary

To prevent build errors, pip packages must be compiled on the same OS as lambda.

## Usage

```
docker build -t netkeiba_lambda . && docker run --rm --env-file=".env" netkeiba_lambda ./update-function-code.sh
```
