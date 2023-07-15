from app_config import AppConfig
from dummy_predictor import DummyPredictor

if __name__ == '__main__':
    appConfig = AppConfig()
    dummy_predictor = DummyPredictor(appConfig)
    dummy_predictor.start()
