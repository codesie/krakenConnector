import hashlib
import hmac
import requests
import json
import base64
import time
import urllib.parse


def generate_nonce():
    """
    Generates the nonce.

    Sources:
    https://www.kraken.com/features/api#general-usage
    https://github.com/veox/python3-krakenex/blob/742aed50e7568a3561b10c439458359b52332e61/krakenex/api.py
    """
    return int(1000 * time.time())


def generate_api_sign(private_path, data, secret):
    """
    Generates the api sign key.

    Sources:
    https://www.kraken.com/features/api#general-usage
    https://github.com/veox/python3-krakenex/blob/742aed50e7568a3561b10c439458359b52332e61/krakenex/api.py
    """
    postdata = urllib.parse.urlencode(data)

    # Unicode-objects must be encoded before hashing
    encoded = (str(data['nonce']) + postdata).encode()
    message = private_path.encode() + hashlib.sha256(encoded).digest()

    signature = hmac.new(base64.b64decode(secret),
                         message, hashlib.sha512)

    sigdigest = base64.b64encode(signature.digest())

    return sigdigest.decode()


class KrakenConnector:
    c_kraken_url = "https://api.kraken.com"

    def __init__(self, config_file):
        self.config_file = config_file
        self.i_api_key = None
        self.i_api_secret = None
        self.get_config()

    def get_config(self):
        """
        Get the content of the config.json file, which includes the amount of euros to spend per trade, which
        currencies to trade and more.

        Returns:
        json:Content of the file
        """
        with open(self.config_file) as file:
            config_content = json.load(file)
        self.i_api_key = config_content["krakenConnector"]["api_key"]
        self.i_api_secret = config_content["krakenConnector"]["secret"]

    def public_call(self, public_path, query_params):
        """
        Executes public api calls. No need for authentication.

        Parameters:
        public_path (str): target of the private api. ex: "/0/public/Ticker"
        query_params (str): query parameters for specifying, what we want. ex: "?pair=XXBTZEUR"

        Returns:
        json:response from the api
        """
        payload = {}
        headers = {}

        url = self.c_kraken_url + public_path + query_params
        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    def private_call(self, private_path, data):
        """
        Executes private api calls. Private calls need authentication, which is implemented in
        this function.

        Parameters:
        private_path (str): target of the private api. ex: "/0/private/AddOrder"
        data (dict): necessary data for the request. ex: {'pair': 'XXBTZEUR', 'type': 'buy', 'ordertype': 'limit', 'price': 47633.1, 'volume': 0.001049690236411235}
        logger (logging): logging handler for writing to the log file
        """
        data["nonce"] = generate_nonce()

        headers = {
            'API-Key': self.i_api_key,
            'API-Sign': generate_api_sign(private_path, data, self.i_api_secret),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        # logger.debug(headers)

        # logger.info(json.dumps(data, indent=2))

        response = requests.request("POST", self.c_kraken_url + private_path, headers=headers, data=data)

        # logger.info(json.dumps(response.json(), indent=2))

        return response.json()
