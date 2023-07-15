class AppConfig:
    trade_symbol = "BTCUSDT"

    # REST API for reading quotes
    rest_api_service = "http://localhost:8089"

    # ZMQ for realtime reading quotes
    trade_stream_pub = "tcp://localhost:4503"

    # ZMQ for creating/canceling orders
    trade_stream_sub = "tcp://localhost:4504"

    # ZMQ for publishing prediction result, this data displayed on th chart
    trade_advice_pub = "tcp://localhost:4505"
