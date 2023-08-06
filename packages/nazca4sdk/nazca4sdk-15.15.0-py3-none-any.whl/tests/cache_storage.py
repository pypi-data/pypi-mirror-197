from nazca4sdk.datahandling.cache.cache_storage import CacheStorage

cache_storage = CacheStorage(False)

# params = {"key": "gruby:p6", "value": "Mikołaj"}
# result = cache_storage.write_keys(params)
# print(result)
result = cache_storage.read_keys(["gruby"])
print(result)
