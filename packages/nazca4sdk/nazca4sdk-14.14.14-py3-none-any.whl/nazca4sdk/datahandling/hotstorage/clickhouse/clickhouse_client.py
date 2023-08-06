import pandas
from pandas import DataFrame
import clickhouse_connect

from nazca4sdk.datahandling.hotstorage.query import Query


class ClickhouseClient:
    def __init__(self):
        self._client = clickhouse_connect.get_client(host='click',
                                                     port=8000,
                                                     username='readonly',
                                                     password='I6DSw4oMO79loo8T')

    def get(self, query: Query) -> DataFrame:
        query = str(query)
        df_stream = self._client.query_df_stream(query)
        dataframes = pandas.DataFrame()
        with df_stream:
            for df in df_stream:
                dataframes = pandas.concat([dataframes, df])
        return dataframes
