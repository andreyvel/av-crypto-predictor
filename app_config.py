class AppConfig:
    trade_symbol = "BTCUSDT"

    # REST API for reading quotes
    rest_api_service = "http://127.0.0.1:8089"

    # ZMQ for realtime reading quotes
    trade_stream_sub = "tcp://127.0.0.1:4503"

    # ZMQ for creating/canceling orders
    trade_command_pub = "tcp://127.0.0.1:4504"

    # ZMQ for publishing prediction result, this data displayed on th chart
    trade_advice_pub = "tcp://127.0.0.1:4506"
