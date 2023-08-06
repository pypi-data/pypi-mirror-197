"""SDK to communicate with Nazca4.0 system """

from pydantic import ValidationError

from nazca4sdk.datahandling.cache.cache_storage import CacheStorage
from nazca4sdk.datahandling.knowledge.knowledge_storage import KnowledgeStorage
from nazca4sdk.datahandling.nazcavariables.nazca_variables_storage import NazcaVariablesStorage
from nazca4sdk.datahandling.variable_historical_info import VariableHistoricalInfo
from nazca4sdk.datahandling.variable_verificator import VariableIntervalSubtractionInfo, VariableType, \
    ForecastForPrediction
from nazca4sdk.system.system_cache import SystemCache
from nazca4sdk.system.user_variables import UserVariables
from nazca4sdk.system.variables import Variables
from nazca4sdk.analytics.analytics import Analytics


class SDK:
    """SDK for Nazca4 system"""

    def __init__(self, https: bool):
        """ Initializing the system, checking connection and caching system configuration
        if https is required then https = True"""

        self._https = https
        self.analytics = Analytics(https)
        self._system_cache = SystemCache(https)
        self.nazca_variables = NazcaVariablesStorage(https)
        self.variables = Variables(self._system_cache)
        self.user_variables = UserVariables()
        self.knowledge = KnowledgeStorage(https)
        self.cache = CacheStorage(https)
        if not self._system_cache.load:
            print("Init SDK failed")

    def _get_modules(self):
        return self._system_cache.modules

    modules = property(_get_modules)

    def read_historical_variable(self, module_name: str,
                                 variable_names: list,
                                 start_date: str,
                                 end_date: str,
                                 page_size: int = 10000):
        """Get paged variables in specific time range

                Args:
                    module_name: name of module,
                    variable_names: list of variable names,
                    start_date: start time of data acquisition
                    end_date: end time of data acquisition
                    page_size: page size

                Returns:
                    array of variable values : Paged Variable values from selected time range

                Example:
                    sdk.read_historical_variable('Module_Name', ['Variable1'],
                         start_date = '2000-01-01T00:00:00',
                         end_date = '2000-01-01T12:00:00',
                         page_size= 100)
                """

        try:
            data = {'module_name': module_name,
                    'variable_names': variable_names,
                    'start_date': start_date,
                    'end_date': end_date,
                    'page_size': page_size}
            variable_info = VariableHistoricalInfo(**data)
            result = self._system_cache.read_historical_variable(variable_info)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

   
   