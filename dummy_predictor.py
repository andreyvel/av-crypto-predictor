from datetime import datetime, timedelta
import json
import time
import threading
import zmq

from app_config import AppConfig
from common.chart_item_dto import ChartItemDto
from common.chart_line_dto import ChartLineDto
from common.json_encoder import EnhancedJSONEncoder
from common.rest_api_service import RestApiService


class DummyPredictor:
    def __init__(self, cfg: AppConfig) -> None:
        self.cfg = cfg
        self.quotes = []
        self.quote_tick = {}
        self.context = zmq.Context()

    def start(self):
        rest_api = RestApiService(self.cfg.rest_api_service)
        self.quotes = rest_api.load_quotes(self.cfg.trade_symbol)

        trade_stream_thread = threading.Thread(target=self.trade_stream_worker)
        trade_stream_thread.start()

        self.predictor_worker()

    def trade_stream_worker(self):
        socket = self.context.socket(zmq.SUB)
        socket.connect(self.cfg.trade_stream_pub)
        socket.setsockopt(zmq.SUBSCRIBE, bytes("", "utf-8"))

        while True:
            # b'{"symbol":"BTCUSDT","event_type":"quote_tick","dateMs":1689426049985,"price":27063.2,"qnt":1024,"source":"emulator"}'
            json_msg = socket.recv()
            data = json.loads(json_msg)
            print(json_msg)

            if data["event_type"] == "quote_tick":
                symbol = data["symbol"]
                price = data["price"]
                self.quote_tick[symbol] = price  # update last price

    def predictor_worker(self):
        socket = self.context.socket(zmq.PUB)
        #socket.bind(self.cfg.trade_advice_pub)
        socket.bind("tcp://*:%s" % 4505)

        while True:
            # At this point should be real ML algorithm
            # in this code only example how to draw elements on the chart

            predict_hours = 24
            cur_dt = datetime.now()
            print(f"Start prediction: {cur_dt}...")

            cur_dt0 = cur_dt + timedelta(hours=1)
            cur_dt1 = cur_dt + timedelta(hours=predict_hours)

            lines = []
            # draw any lines, for example support levels
            lines.append(ChartLineDto(cur_dt0, 1.5, cur_dt1, 1.5, "PCT", "#008800"))
            lines.append(ChartLineDto(cur_dt0, 1.7, cur_dt1, 1.7, "PCT", "#009900"))
            lines.append(ChartLineDto(cur_dt0, -1.5, cur_dt1, -1.5, "PCT", "#880000"))
            lines.append(ChartLineDto(cur_dt0, -1.7, cur_dt1, -1.7, "PCT", "#990000"))

            items = []
            for ix, hour in enumerate(range(predict_hours)):
                # predict percent change from current price
                next_dt = cur_dt + timedelta(hours=hour + 1)
                predict_pct_up = 0.5 + (ix / 15)
                items.append(ChartItemDto(next_dt, predict_pct_up, "PCT", "0", 2 + (ix / 3), "#559955"))

                predict_pct_down = -0.5 - (ix / 15)
                items.append(ChartItemDto(next_dt, predict_pct_down, "PCT", "0", 2 + (ix / 3), "#995555"))

            last_price = self.quote_tick.get(self.cfg.trade_symbol)
            if last_price:
                # draw same image on the chart
                items.append(ChartItemDto(cur_dt1, 0.5, "PCT", "0", 10, "#559999"))
                items.append(ChartItemDto(cur_dt1, -0.5, "PCT", "0", 10, "#995599"))

            json_obj = {}
            json_obj["chartLines"] = lines
            json_obj["chartItems"] = items

            json_msg = json.dumps(json_obj, cls=EnhancedJSONEncoder)
            socket.send(bytes(json_msg, "utf-8"))
            time.sleep(1)
