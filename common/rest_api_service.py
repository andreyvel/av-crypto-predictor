import json
import urllib.request
from common.quote_bar import QuoteBar


class RestApiService:

    def __init__(self, rest_api_service: str) -> None:
        self.rest_api_service = rest_api_service

    def load_quotes(self, symbol: str) -> list:
        params = "symbol=" + symbol + "&interval=5m&limit=1000"
        url_quotes = self.rest_api_service + "/quotes?" + params
        print(f"Loading quotes {url_quotes}")

        quote_list = []
        with urllib.request.urlopen(url_quotes) as f:
            # {"result":[{"date":"2023-07-15T12:30","high":27008.15,"vol":0,"low":26976.02,"close":27005.96,"open":27003.5}...
            json_msg = f.read()

        data = json.loads(json_msg)
        result = data["result"]

        for row in result:
            bar = QuoteBar(row)
            quote_list.append(bar)

        print(f"Loaded {len(quote_list)} rows {symbol}")
        return quote_list
