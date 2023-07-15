from dataclasses import dataclass


@dataclass
class ChartItemDto:
    date: str
    value: float
    unit: str  # ABS - absolute value, PCT - value calculate relative last price as increment percent

    shape: str  # 0 - circle
    radius: int  # radius of circle
    color: str  # example #008800
