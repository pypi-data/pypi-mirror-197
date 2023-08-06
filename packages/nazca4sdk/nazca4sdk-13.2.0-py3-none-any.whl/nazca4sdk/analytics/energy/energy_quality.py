"""Module to calculate energy quality according to EN50160"""
from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient


class EnergyQuality:
    """ Class to send and receive information from Energy quality module in brain"""

    def __init__(self):
        self.energy_brain = BrainClient()

    def calculate_energy_quality(self, module: str):
        """
        Function to determine energy quality values for determined input

        Args:
            module: module name
        Returns:
            ::energy quality parameters -> dictionary with energy quality parameters::
            (worstCaseQuality: Overall energy quality;
            worstCaseQuality1: Overall energy quality of phase 1;
            worstCaseQuality2 Overall energy quality of phase 2;
            worstCaseQuality3: Overall energy quality of phase 3;
            frequencyQuality1: Overall frequency quality of phase 1;
            voltageQuality1: Overall voltage quality of phase 1;
            cosQuality1: Overall cosinus quality of phase 1;
            thdQuality1: Overall thd quality of phase 1;
            frequencyQuality2: Overall frequency quality of phase 2;
            voltageQuality2: Overall voltage quality of phase 2;
            cosQuality2: Overall cosinus quality of phase 2;
            thdQuality2: Overall thd quality of phase 2;
            frequencyQuality3: Overall frequency quality of phase 3;
            voltageQuality3: Overall voltage quality of phase 3;
            cosQuality3: Overall cosinus quality of phase 3;
            thdQuality3: Overall thd quality of phase 3;
        """

        try:
            response = self.energy_brain.get_energy_quality(module)
            result = self.energy_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None
