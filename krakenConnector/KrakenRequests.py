from .KrakenConnector import KrakenConnector


class KrakenRequests(KrakenConnector):
    def __init__(self, config_file):
        super().__init__(config_file)

    def get_kraken_data(self, pair):
        """
        Get price information about currency pairs.

        @param {list} pair - currency pair
            ex1. ["SOLEUR"]
            ex2. ["ETHEUR", "DOTEUR"]

        @returns {dict}
            ex. {'error': [], 'result': {'SOLEUR': {...}}}
        """
        query_params = "?pair=" + ",".join(pair)

        ticker_result = self.public_call("/0/public/Ticker", query_params)

        return ticker_result

    def query_order(self, data):
        """
        Get order information.

        :param {dict} data:
            ex. {
                    "txid": "TGTHGO-OBCX4-ISL83U"
                }

        :return: {dict}
            ex:
        """
        result = self.private_call("/0/private/QueryOrders", data)

        return result

    def create_order(self, data):
        """
        Create an order.

        :param {dict} data:
            ex. {
                    "pair": "SOLEUR",
                    "type": "buy",
                    "ordertype": "limit",
                    "price": 168.65,
                    "volume": 0.316542
                }

        :return: {dict}
            ex:
                {
                    "error": [],
                    "result": {
                        "txid": ["TGTHGO-OBCX4-ISL83U"],
                        "descr": {
                            "order": "buy 0.31918289 SOLEUR @ limit 156.65"
                        }
                    }
                }
        """
        result = self.private_call("/0/private/AddOrder", data)

        return result
