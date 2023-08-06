"""SDK to communicate with Nazca4.0 system """

from nazca4sdk.analytics.analytics import Analytics
from nazca4sdk.datahandling.cache.cache_storage import CacheStorage
from nazca4sdk.datahandling.knowledge.knowledge_storage import KnowledgeStorage
from nazca4sdk.datahandling.nazcavariables.nazca_variables_storage import NazcaVariablesStorage
from nazca4sdk.system.system_cache import SystemCache
from nazca4sdk.system.user_variables import UserVariables
from nazca4sdk.system.variables import Variables


class SDK:
    """SDK for Nazca4 system"""

    def __init__(self, https: bool):
        """ Initializing the system, checking connection and caching system configuration
        if https is required then https = True"""

        self._https = https
        self._system_cache = SystemCache(https)
        self.analytics = Analytics(https) #: analytics functions 
        self.nazca_variables = NazcaVariablesStorage(https) #: read nazca variables 
        self.variables = Variables(self._system_cache) #: read device variables and variables statistics 
        self.user_variables = UserVariables() #: read and write user variables and user variables statistics 
        self.knowledge = KnowledgeStorage(https) #: read, write and delete knowledge 
        self.cache = CacheStorage(https) # read and write cache value
        if not self._system_cache.load:
            print("Init SDK failed")

    def _get_modules(self):
        return self._system_cache.modules

    modules = property(_get_modules)
