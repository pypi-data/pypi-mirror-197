""" Module to communicate with Brain"""
import requests
from nazca4sdk.datahandling.data_mod import Data


class BrainClient:
    """ Get data from Nazca4.0 Brain
    """

    def __init__(self):
        """Initialize Brain connection info"""
        self.__brain_url = 'http://10.217.10.80:10334'

    def get_energy_quality(self, module: str):
        """ Posting data to receive energy quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/energy/', json={"moduleName":module})

    def get_vibration_quality(self, group: str, module: str):
        """ Posting data to receive vibration quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/vibration/', json={"moduleName": module, "group":group})

    def get_oee_easy(self, oee_easy_input):
        """ Posting data to receive OEE value based on:
            Availability, Performance, Quality parameters from Brain """
        return requests.post(f'{self.__brain_url}/oee_easy/', json=oee_easy_input)

    def get_oee_full(self, oee_full_input):
        """ Posting data to receive oee value based on A, B, C, D, E, F parameters from Brain"""
        return requests.post(f'{self.__brain_url}/oee_full/', json=oee_full_input)

    def get_cp_pp_indicator(self, cp_pp_input):
        """
        Posting data to receive cp/pp indicator based on:
            lsl, usl, std parameters from Brain
        """

        return requests.post(f'{self.__brain_url}/cp_pp_indicator/', json=cp_pp_input)

    def get_cpk_ppk_indicator(self, cpk_ppk_input):
        """
        Posting data to receive cpk/ppk indicator based on:
            lsl, usl, mean, std parameters from Brain
        """
        return requests.post(f'{self.__brain_url}/cpk_ppk_indicator/', json=cpk_ppk_input)

    def get_prediction(self, prediction_input):
        """
        Posting data to receive prediction value based on: module_name, variable_name, time_amount, time_unit,
        forecast_time_amount, forecast_unit parameters from Brain
        """
        return requests.post(f'{self.__brain_url}/prediction/', json=prediction_input)

    @staticmethod
    def parse_response(response):
        """ Parsing method"""
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Brain response failure")
                return None
            return json_response
        print("Brain response error")
        return None
