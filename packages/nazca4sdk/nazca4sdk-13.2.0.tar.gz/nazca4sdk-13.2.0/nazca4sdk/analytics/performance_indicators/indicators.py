"""Module to calculate KPIs"""
from pandas import DataFrame
import pandas as pd
import numpy as np
from pydantic import ValidationError
from nazca4sdk.analytics.performance_indicators.oee_calculations import Oee
from nazca4sdk.analytics.performance_indicators.process_indicators import ProcessIndicators

d2 = [1.128, 1.1693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078, 3.173, 3.259, 3.336, 3.407, 3.472, 3.532,
      3.588, 3.64, 3.689, 3.735, 3.778, 3.819, 3.858, 3.895, 3.931, 3.964, 3.997, 4.027, 4.057, 4.086]


class Indicators:
    """
    Indicators module with key performance indicators functions
    """

    def __init__(self):
        self.oee = Oee()
        self.process_indicators = ProcessIndicators()

    def get_oee_simple(self, availability: float, performance: float, quality: float):
        """The Overall Equipment Effectiveness (OEE)

        The Overall Equipment Effectiveness (OEE) is a proven way to monitor
        and improve process efficiency.
        it is considered as a diagnostic tool since it does not provide a solution to a given problem.
        OEE is a key process indicator that measures effectiveness and deviations
        from effective machine performance.

        OEE is calculated as:
            OEE = Availability x Performance x Quality
        Args:
            availability: float
            performance: float
            quality: float

        Return:
            OEE value: float

        Example:
            get_oee_simple(availability: 50, performance: 30, quality: 60)
        """
        try:
            data = {"availability": availability,
                    "performance": performance,
                    "quality": quality
                    }
            result = self.oee.calculate_oee_simple(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_oee_complex(self, a: float, b: float, c: float, d: float, e: float, f: float):
        """The Overall Equipment Effectiveness (OEE)

        The Overall Equipment Effectiveness (OEE) is a proven way to monitor
        and improve process efficiency.
        it is considered as a diagnostic tool since it does not provide a solution to a given problem.
        OEE is a key process indicator that measures effectiveness and deviations
        from effective machine performance.

        Args:
        OEE depends on parameters as follows:
            A = Total available time
            B = Run time
            C = Production capacity
            D = Actual production
            E = Production output (same as actual production)
            F = Actual good products (i.e. product output minus scraps)
        where,
        A and B define Availability,
        C and D define Performance,
        E and F define Quality

        OEE is calculated as:

        OEE = (B/A) x (D/C) x (F/E)

        Returns:
            OEE value: float

        Example:
            get_oee_complex(A: 50, B: 40, C: 60, D: 20, E: 100, F: 10)
        """
        try:
            data = {"A": a,
                    "B": b,
                    "C": c,
                    "D": d,
                    "E": e,
                    "F": f
                    }
            result = self.oee.calculate_oee_complete(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_availability(self, run_time: float, total_time: float):
        """Availability

            Takes into account availability/time loss, which includes all events
            related to unplanned stops.
            (e.g. equipment failures, material shortages) and planned stops (e.g. changeover times).
            Availability measures the proportion of time a machine or cell runs
            from the total theoretical available time.
            Calculated as:
                Availability = Run time/Total available time
            Args:
                ::input -> dictionary with oee parameters::
                run_time, Run time in hours
                total_time, Total run time in hours

            Returns:
                availability value: float

            Example:
                get_availability(run_time: 30, total_time: 50)
            """
        try:
            data = {"run_time": run_time,
                    "total_time": total_time,
                    }
            result = self.oee.calculate_availability(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_performance(self, actual_production: float, production_capacity: float):
        """Performance

            Takes into account performance/speed loss, which includes all the factors
            (e.g. slow cycles, small stops)
            that prevent the machine or cell to operate at maximum/optimal speed.
            It measures the proportion of produced units from the total number of possible
            produced units in a given run.

            Calculated as:
                Performance = Actual production/Production capacity

            Args:
                ::performance_input -> dictionary with performance parameters::
                actual_production, actual production
                production_capacity, production capacity

            Returns:
                performance value: float

            Example:
                get_performance(actual_production: 30, production_capacity: 50)
            """
        try:
            data = {"actual_production": actual_production,
                    "production_capacity": production_capacity,
                    }
            result = self.oee.calculate_availability(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_quality(self, actual_products: float, production_output: float):
        """Quality

            Takes into account quality loss, which includes all the factors
            (e.g. reworks, scraps, defects).
            that lead to defective units that do not meet the customer’s quality
            standards and specifications.
            Quality measures the proportion of non-defective units compared
            to the total units produced.
            Calculated as:
                Quality = Actual good products/Product output
            Args:
                ::quality_input -> dictionary with performance parameters::
                actual_products, Actual good products
                production_output, Production output

            Returns:
                quality value: float

            Example:
                get_quality(actual_products: 30, production_output: 50)
            """
        try:
            data = {"actual_products": actual_products,
                    "production_output": production_output,
                    }
            result = self.oee.calculate_quality(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def __estimate_std_using_time(self, samples, offset, count):
        """
        The function to estimate standard deviation for Cp/Cpk indicator using time offset

        Args:
            samples: DataFrame with samples
            offset: time offset in seconds
            count: number of samples in subgroups

        Return:
            estimated standard deviation
        """
        ranges = []
        start = samples.head(1).measureTime
        time = start

        while time.values < samples.tail(1).measureTime.values:
            data = (samples[samples['measureTime'].values >
                            time.values].iloc[0:count])
            if data.shape[0] == count:
                ranges.append(max(data.value) - min(data.value))
            time = time + pd.DateOffset(seconds=offset)
        return np.mean(ranges) / d2[count - 2]

    def __estimate_std_using_samples(self, samples, offset, count):
        """
        The function to estimate standard deviation for Cp/Cpk indicator using samples offset

        Args:
            samples: DataFrame with samples
            offset: number of samples between subgroups
            count: number of samples in subgroups

        Return:
            estimated standard deviation
        """
        ranges = []
        idx = samples.index[0]
        while idx < samples.index[-1]:
            data = (samples.iloc[idx:idx + count])
            if data.shape[0] == count:
                ranges.append(max(data.value) - min(data.value))
            idx = idx + offset
        return np.mean(ranges) / d2[count - 2]

    def get_cp_indicator(self, lsl: float, usl: float, period: int, subgroups: int, samples: DataFrame,
                         estimation_type='samples'):
        """
        The function to calculate Process Capability Indicator (Cp):

        Cp indicator is calculated as:

            Cp = (USL-LSL)/(6*std)
        Args:
            lsl : lower specification limit,
            usl : upper specification limit,
            period: when estimation_type = 'samples', this is number of samples,
            for estimation_type = 'time' this is number of seconds
            subgroups: number of samples in subgroups,
            samples: DataFrame with samples,
            estimation_type: 'time' to estimate std using time offset or 'samples'
            to estimate using number of samples offset

        Return:
            Cp value

        """
        try:
            if estimation_type == 'samples':
                std = self.__estimate_std_using_samples(
                    samples, period, subgroups)
            elif estimation_type == 'time':
                std = self.__estimate_std_using_time(
                    samples, period, subgroups)
            else:
                raise ValueError(
                    "Invalid estimation type. Expected 'time' or 'samples'")

            data = {"name": 'Cp',
                    "lsl": lsl,
                    "usl": usl,
                    "std": std
                    }

            result = self.process_indicators.calculate_cp_pp_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_pp_indicator(self, lsl: float, usl: float, samples: DataFrame):
        """
        The function to calculate Process Performance Indicator (Pp):

        Pp indicator is calculated as:

            Pp = (USL-LSL)/(6*std)
        Args:
            lsl : lower specification limit,
            usl : upper specification limit,
            samples: DataFrame with samples

        Return:
            Pp value

        """
        try:
            std = samples.value.std()
            data = {"name": 'Pp',
                    "lsl": lsl,
                    "usl": usl,
                    "std": std
                    }
            result = self.process_indicators.calculate_cp_pp_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_cpk_indicator(self, lsl: float, usl: float, period: float, subgroups: int, samples: DataFrame):
        """
        The function to calculate Process Capability Index (Cpk):

        Cpk indicator is calculated as:

            Cpk = min(upper, lower)

            where:
                upper = (USL - mean)/(3*std)
                lower = (mean - LSL)/(3*std)

        Args:
            lsl: lower specification limit,
            usl: upper specification limit,
            period: number of samples between subgroups,
            subgroups: number of samples in subgroups,
            samples: DataFrame with samples

        Return:
            Pp value: float
        """
        try:
            std = self.__estimate_std_using_samples(samples, period, subgroups)
            mean = samples.value.mean()
            data = {"name": 'Cpk',
                    "lsl": lsl,
                    "usl": usl,
                    "mean": mean,
                    "std": std
                    }
            result = self.process_indicators.calculate_cpk_ppk_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_ppk_indicator(self, lsl: float, usl: float, samples: DataFrame):
        """
        The function to calculate Process Performance Index (Ppk):

        Ppk indicator is calculated as:

            Ppk = min(upper, lower)

            where:
                upper = (USL - mean)/(3*std)
                lower = (mean - LSL)/(3*std)

        Args:
            lsl : lower specification limit,
            usl : upper specification limit,
            samples: DataFrame with samples

        Return:
            Ppk value

        """
        try:
            std = samples.value.std()
            mean = samples.value.mean()
            data = {"name": 'Ppk',
                    "lsl": lsl,
                    "usl": usl,
                    "mean": mean,
                    "std": std
                    }
            result = self.process_indicators.calculate_cpk_ppk_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None
