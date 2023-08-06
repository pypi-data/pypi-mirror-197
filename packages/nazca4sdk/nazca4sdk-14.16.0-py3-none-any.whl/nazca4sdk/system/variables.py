from datetime import datetime
from typing import Optional

import pandas as pd
from pandas import DataFrame
from pydantic import ValidationError

from nazca4sdk.datahandling.hotstorage.clickhouse.clickhouse_client import ClickhouseClient
from nazca4sdk.datahandling.hotstorage.query import Query
from nazca4sdk.datahandling.variable_historical_info import VariableHistoricalInfo
from nazca4sdk.datahandling.variable_verificator import VariableIntervalInfo, DATE_TIME_FORMAT, \
    VariableIntervalSubtractionInfo
from nazca4sdk.system.system_cache import SystemCache
from nazca4sdk.tools.time import get_time_delta


class Variables:
    def __init__(self, cache: SystemCache):
        self._system_cache = cache
        self._clickhouse_client = ClickhouseClient()

    def list(self):
        return self._system_cache.variables

    def read(self, module_name: str, variable_names: list, **time: dict) -> Optional[DataFrame]:
        """
        Gets variable in specific time range by connection with open database

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            time - Possible pairs: start_date, end_date or time_amount, time_unit

        Returns:
            DataFrame: values for selected variable and time range
        """

        keys = time.keys()
        if "start_date" in keys and "end_date" in keys:
            print("variable over day")
            data = {'module_name': module_name,
                    'variable_names': variable_names,
                    'start_date': time.get("start_date"),
                    'end_date': time.get("end_date")}
            variable_info = VariableIntervalInfo(**data)
            return self._variable_over_day(variable_info.module_name,
                                           variable_info.variable_names,
                                           datetime.strptime(variable_info.start_date, DATE_TIME_FORMAT),
                                           datetime.strptime(variable_info.end_date, DATE_TIME_FORMAT))
        elif "time_amount" in keys and "time_unit" in keys:
            print("variable over time")
            time_amount = time.get("time_amount")
            time_unit = time.get("time_unit")
            data = {'module_name': module_name,
                    'variable_names': variable_names,
                    'time_amount': time_amount,
                    'time_unit': time_unit}
            variable_info = VariableIntervalSubtractionInfo(**data)

            end_date = datetime.now()
            start_date = end_date - get_time_delta(time_unit, time_amount)
            return self._variable_over_day(variable_info.module_name,
                                           variable_info.variable_names,
                                           start_date,
                                           end_date)

        print("time should contains start_date and end_date or time_unit and time_amount")
        return None

    def stats(self, module: str, variables: [str], start_date: str, end_date: str) -> Optional[DataFrame]:
        """ Read module variable stats

        Args:
            module: module name
            variables: list of variable names
            start_date: start of date range
            end_date: end of date range
        Returns:
            VariableStats list
        """
        return self._read_variables_stats(module=module, variables=variables, start_date=start_date, end_date=end_date)

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
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def _read_variables_stats(self, module: str, variables: [str], start_date: str, end_date: str)\
            -> Optional[DataFrame]:
        exist_vars = self._system_cache.check_if_exist(module, variables)
        if not exist_vars:
            print(f"Module {module} or  variables {variables} not exist")
            return None
        variables_grouped = self._system_cache.group_variables(module, variables)
        # check variables type
        for element in variables_grouped:
            if element[0] not in self._system_cache.stats_variable_type:
                print("Variable to count stats should be type of:")
                for element_type in self._system_cache.stats_variable_type:
                    print(f" -  {element_type}")
                print(f"Variables {element[1]} is type of {element[0]}")
                return None
        # variables_stats_info = VariableStatsInfo(module=module, startDate=start_date, endDate=end_date,
        #                                          variables=variables_grouped)

        dataframe = pd.DataFrame()
        for key, value in variables_grouped:
            variables_list = ",".join([f"'{item}'" for item in value])
            query = Query() \
                .SELECT("Module, Variable, toFloat32(min(Value)) as Min, "
                        "toFloat32(max(Value)) as Max, toFloat64(avg(Value)) as Avg, "
                        "toFloat32(anyLast(Value)) as LastValue, toFloat64(varPop(Value)) as Variance, "
                        "toFloat64(stddevPop(Value)) as Std ") \
                .FROM(f"nazca.devices_data_{key}") \
                .WHERE(f"Module like '{module}' and "
                       f"MeasureTime >= '{start_date}' "
                       f"and MeasureTime <= '{end_date}' "
                       f"and Variable IN ({variables_list})") \
                .GROUP_BY("Module, Variable")
            df = self._clickhouse_client.get(query)
            dataframe = pd.concat([dataframe, df])
        return dataframe

    def _variable_over_day(self, module_name, variable_names, start_date, end_date) -> Optional[DataFrame]:
        """
        Gets variable in specific time range by connection with open database

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            start_time - beginning of the time range
            stop_time - ending of the time range

        Returns:
            DataFrame: values for selected variable and time range

        """

        try:
            exist_vars = self._system_cache.check_if_exist(module_name, variable_names)
            if not exist_vars:
                print(f"Module {module_name} or {variable_names} not exist")
                return None
            variables_grouped = self._system_cache.group_variables(
                module_name, variable_names)

            dataframe = pd.DataFrame()
            for group in variables_grouped:
                table = group[0]
                variables = ",".join([f"'{item}'" for item in group[1]])
                query = Query() \
                    .SELECT("*") \
                    .FROM(f"nazca.devices_data_{table}") \
                    .WHERE(f"Module like '{module_name}' "
                           f"and MeasureTime >= '{start_date.strftime('%Y-%m-%dZ%H:%M:%S')}' "
                           f"and MeasureTime <= '{end_date.strftime('%Y-%m-%dZ%H:%M:%S')}' "
                           f"and Variable IN ({variables})")
                df = self._clickhouse_client.get(query)
                dataframe = pd.concat([dataframe, df])
            return dataframe
        except ValueError:
            print("Error - Get variable data from Nazca4")
            return None
