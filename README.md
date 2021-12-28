# krakenConnector
Easy way to interact with the kraken crypto exchange api.

# How To

## Install krakenConnector

### Download
First we need to download the krakenConnector. Let's store the download for example in the `/opt/` directory. The full
path would look likes this `/opt/krakenConnector/`.

### Install
```Hint: It works best, if the package `wheel` is installed before trying to install `krakenConnector`.```

While we are in our python virtual environment we can install the package like this:

```bash
pip install /opt/krakenConnector/
```

The installation can be verified with `pip list`.


## Pre-requirements
The krakenConnector requires a config file in the json format, which contains the api key and secret.
These need to be generated on kraken.

```json
{
  "krakenConnector": {
    "api_key": "API-KEY-API-KEY from kraken",
    "secret": "API-SECRET-API-SECRET from kraken"
  }
}
```

## Use krakenConnector
example.py
```py
from krakenConnector import KrakenRequests
import json

krqsts = KrakenRequests(
    "/mnt/linuxData/crypto/example-krakenConnector/krakenConnector.json")

result = krqsts.get_kraken_data(["SOLEUR"])

print(json.dumps(result, indent=2))
```

response as json
```json
{
  "error": [],
  "result": {
    "SOLEUR": {
      "a": [
        "175.01000",
        "9",
        "9.000"
      ],
      "b": [
        "175.00000",
        "52",
        "52.000"
      ],
      "c": [
        "174.87000",
        "2.63140467"
      ],
      "v": [
        "9901.83132395",
        "18993.81695583"
      ],
      "p": [
        "172.69526",
        "171.30897"
      ],
      "t": [
        1665,
        2861
      ],
      "l": [
        "168.70000",
        "167.67000"
      ],
      "h": [
        "176.06000",
        "176.06000"
      ],
      "o": "170.87000"
    }
  }
}
```