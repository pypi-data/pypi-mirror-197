from pydantic import ValidationError

from nazca4sdk.datahandling.cache.key_value import KeyValue
from nazca4sdk.datahandling.open_data_client import OpenDataClient


class CacheStorage:
    """Allow user to read and write value to Cache

    """

    def __init__(self, https: bool):
        self.__openData = OpenDataClient(https)

    def read_keys(self, keys):
        """Read cache values for list of keys
        
        Args:
            keys - list of keys to read
        Returns:
            List of cache entry
        """
        return self.__openData.read_cache_keys(keys)

    def write_keys(self, key: str, value):
        """write key value to cache

        Args:
            key: key
            value: value to write to cache
        Returns:
            CacheEntry if success or None if error
        """

        data = {'key': key,
                'value': value}
        try:
            variable_info = KeyValue(**data)
            return self.__openData.write_cache_keys(variable_info)
        except ValidationError as error:
            print(error.json())
            return None


