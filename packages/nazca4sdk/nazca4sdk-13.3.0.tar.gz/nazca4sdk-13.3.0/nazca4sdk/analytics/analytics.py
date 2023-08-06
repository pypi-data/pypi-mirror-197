"""Analytics module"""
from nazca4sdk.analytics.performance_indicators.indicators import Indicators
from nazca4sdk.analytics.energy.energy_quality import EnergyQuality
from nazca4sdk.analytics.vibration.vibration_quality import VibrationQuality
from nazca4sdk.analytics.prediction.forecasting import Forecasting


class Analytics:
    """
    Analytics module as a second layer of analytics functions to use with SDK
    """

    def __init__(self, https: bool):
        self.kpi = Indicators()
        self.energy = EnergyQuality()
        self.vibration = VibrationQuality()
        self.forecasting = Forecasting(https)
