from datetime import datetime
from dataclasses import dataclass


@dataclass
class ChartLineDto:
    date0: datetime
    value0: float

    date1: datetime
    value1: float

    unit: str  # ABS - absolute value, PCT - value calculate relative last price as increment percent
    color: str  # example #008800
