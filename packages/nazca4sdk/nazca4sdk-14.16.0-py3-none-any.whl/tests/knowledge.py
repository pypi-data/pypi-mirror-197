from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.sdk import SDK
from nazca4sdk import FormatChart, FormatText
import requests
import datetime


sdk = SDK(False)
# odczyt dla danego klucza

# delete knowledge
sdk.write_knowledge("pomidor1", "sekcja pomidor1", "test", KnowledgeDataType.TEXT)
sdk.write_knowledge("pomidor1", "sekcja pomidor2", "test", KnowledgeDataType.TEXT)
sdk.write_knowledge("pomidor1", "sekcja pomidor3", "test", KnowledgeDataType.TEXT)

result = sdk.delete_knowledge_sections(["sekcja pomidor1", "sekcja pomidor2"], "pomidor1")

result = sdk.write_knowledge("pomidor1", "sekcja pomidor", "test", KnowledgeDataType.TEXT)
result2 = sdk.write_knowledge("pomidor2", "sekcja pomidor", "test", KnowledgeDataType.TEXT)
deleted_documents = sdk.delete_knowledge_keys(["pomidor1", "pomidor2"])

values = sdk.read_knowledge("test")
keys = sdk.read_knowledge_keys("test", "2023-01-01T00:00:00", "2023-01-11T00:00:00", "0")
keys2 = sdk.read_knowledge_keys("test", "2023-01-01T00:00:00")
keys3 = sdk.read_knowledge_keys("test")
keys4 = sdk.read_knowledge_keys(size=4)
#print(values)

# result = sdk.write_knowledge("blob", "pliczek", "/2022-07-07_14-31.png", KnowledgeDataType.BLOB)
#result = sdk.write_knowledge("gruby", "sekcjaGruby", "test", KnowledgeDataType.TEXT)
#print(result)










