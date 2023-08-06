from nazca4sdk.sdk import SDK

sdk = SDK(False)
sdk.modules
sdk.variables
#print(sdk.read_variables_stats('symulator', ['P1', 'Q1'], '2023-01-24T00:00:00', '2023-01-24T23:00:00'))