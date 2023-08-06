"""Module to calculate vibration quality"""
from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient
from nazca4sdk.datahandling.variable_verificator import VibrationInput


class VibrationQuality:
    """ Class to send and receive information from Vibration quality module in brain"""

    def __init__(self):
        self.vibration_brain = BrainClient()

    def calculate_vibration_quality(self, group: str, module: str):
        """Function to determine vibration quality values for determined input

        Args:
            group: group name
            module: module name

        Returns:
            dict: vibration quality parameters
        """

        try:
            response = self.vibration_brain.get_vibration_quality(group, module)
            result = self.vibration_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None
