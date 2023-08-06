from nazca4sdk.sdk import SDK

sdk = SDK(False)

print(sdk.predict('symulator', 'V1', 5, 'MINUTE', 3, 'min', 'prophet'))
