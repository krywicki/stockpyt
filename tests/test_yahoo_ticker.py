import os, json, requests, pytest

from stockpyt import StockQuote
from stockpyt.tickers import YahooTickerAgent

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources", "yahoo")

class MockResponse(requests.Response):
    def __init__(self, data:dict):
        self.data = data

    def json(self, *args, **kwargs):
        return self.data

# Test Fixtures
# -----------------------

@pytest.fixture(scope="module")
def google_data() -> dict:
    with open(os.path.join(RESOURCE_DIR, "googl.json")) as f:
        data = json.load(f)
    yield data

@pytest.fixture(scope="module")
def plug_data() -> dict:
    with open(os.path.join(RESOURCE_DIR, "plug.json")) as f:
        data = json.load(f)
    yield data

# Tests
# -----------------------

def test_general_network_requests():
    """ ensure no network responses are good """

    agent = YahooTickerAgent()
    quotes = agent.get_quotes(["GOOGL", "IBM", "INTC", "AAPL"])

    for quote in quotes:
        assert quote.err == ""

def test_googl(google_data):
    """ test google finance data """

    agent = YahooTickerAgent()
    resp = MockResponse(google_data)

    quote:StockQuote = agent._parse_resp(resp)

    assert quote.symbol                 == "GOOGL"
    assert round(quote.open, 2)         == 1667.44
    assert round(quote.prev_close, 2)   == 1556.88
    assert round(quote.price, 2)        == 1616.11
    assert round(quote.high, 2)         == 1681.31
    assert round(quote.low, 2)          == 1601.57
    assert quote.perc_change            == -((quote.prev_close - quote.price) / quote.prev_close) * 100.0

def test_plug(plug_data):
    """ test plug finance data """

    agent = YahooTickerAgent()
    resp = MockResponse(plug_data)

    quote:StockQuote = agent._parse_resp(resp)

    assert quote.symbol                 == "PLUG"
    assert round(quote.open, 2)         == 14.65
    assert round(quote.prev_close, 2)   == 14.81
    assert round(quote.price, 2)        == 14.00
    assert round(quote.high, 2)         == 14.81
    assert round(quote.low, 2)          == 13.69
    assert quote.perc_change            == -((quote.prev_close - quote.price) / quote.prev_close) * 100.0
