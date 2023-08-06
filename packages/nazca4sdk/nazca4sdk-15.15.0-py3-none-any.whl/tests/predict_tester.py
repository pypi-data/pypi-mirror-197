from nazca4sdk.sdk import SDK

sdk = SDK(False)

print(sdk.analytics.forecasting.predict('lol', 'V1', 74, 'MINUTE', 1, 'min', 'prophet'))
