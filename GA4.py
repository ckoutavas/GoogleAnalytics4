import pandas as pd
import numpy as np
from typing import List, Optional, Literal
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (DateRange, Dimension, Metric, FilterExpression,
                                                Filter, RunReportRequest, NumericValue)


# noinspection PyTypeChecker
class BuildReport:
    def __init__(self, property_id: str, ga_dimensions: List[str], ga_metrics: List[str],
                 start_date: str, end_date: str, creds_path: Optional[str] = None) -> None:
        """
        This builds a GA4 report that can be run with or without a filter

        Dimension and metrics can be found by visiting:
        https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema

        start_date
            The inclusive start date for the query in the format
            ``YYYY-MM-DD``. Cannot be after ``end_date``. The format
            ``NdaysAgo``, ``yesterday``, or ``today`` is also accepted,
            and in that case, the date is inferred based on the
            property's reporting time zone.

        end_date
            The inclusive end date for the query in the format
            ``YYYY-MM-DD``. Cannot be before ``start_date``. The format
            ``NdaysAgo``, ``yesterday``, or ``today`` is also accepted,
            and in that case, the date is inferred based on the
            property's reporting time zone.

        SAMPLE CODE

        import GA4

        report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

        :param property_id: GA4 property id
        :param ga_dimensions: list of GA4 dimensions you want to return
        :param ga_metrics: list of GA4 metrics you want to return
        :param start_date: pull data starting from this date
        :param end_date: pull data ending on this date
        :param creds_path: if specified use credentials.json path and not the environment variable
        """
        self.dimension_filter = None
        self.dimensions = [Dimension(name=x) for x in ga_dimensions]
        self.metrics = [Metric(name=x) for x in ga_metrics]
        self.date_ranges = [DateRange(start_date=start_date, end_date=end_date)]
        self.property_id = property_id

        if creds_path:
            self.client = BetaAnalyticsDataClient.from_service_account_json(creds_path)
        else:
            self.client = BetaAnalyticsDataClient()

    def add_filter(self,
                   filter_type: Literal['string_filter', 'in_list_filter', 'numeric_filter', 'between_filter'],
                   field_name: str,
                   filter_values: Optional[List[str] | str | NumericValue] = None,
                   filter_case: Optional[bool] = False,
                   match_type: Optional[Filter.StringFilter.MatchType] = Filter.StringFilter.MatchType(0),
                   operation: Optional[Filter.NumericFilter.Operation] = Filter.NumericFilter.Operation(0),
                   from_value: Optional[NumericValue] = None,
                   to_value: Optional[NumericValue] = None) -> None:
        """
        This adds a filter to the BuildReport object. This is not required - i.e., BuildReport objects can be run
        without a filter

        The match_type of a string filter
            MATCH_TYPE_UNSPECIFIED = 0
            EXACT = 1
            BEGINS_WITH = 2
            ENDS_WITH = 3
            CONTAINS = 4
            FULL_REGEXP = 5
            PARTIAL_REGEXP = 6

        The operation applied to a numeric filter
            OPERATION_UNSPECIFIED = 0
            EQUAL = 1
            LESS_THAN = 2
            LESS_THAN_OR_EQUAL = 3
            GREATER_THAN = 4
            GREATER_THAN_OR_EQUAL = 5

        SAMPLE CODE

        import GA4

        report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')


        report.add_filter(filter_type='string_filter',
                          field_name='pagePath',
                          match_type=Filter.StringFilter.MatchType.EXACT,
                          filter_values='/Page/1',
                          filter_case=True)

        :param filter_type: select one of the four filter types
        :param field_name: the dimensions to filter on
        :param filter_values: the value to be used in the filter
        :param filter_case: is the filter value case-sensitive
        :param match_type: only used with a StringFilter
        :param operation: only used with a NumericFilter
        :param from_value: only used with BetweenFilter
        :param to_value: only used with BetweenFilter
        """

        literals = ['string_filter', 'in_list_filter', 'numeric_filter', 'between_filter']
        if filter_type not in literals:
            raise ValueError(f"filter_type must be 'string_filter', 'in_list_filter', 'numeric_filter' "
                             f"or 'between_filter' you entered '{filter_type}'")

        if filter_type == 'string_filter':
            self.dimension_filter = FilterExpression(filter=Filter(field_name=field_name,
                                                                   string_filter=Filter.StringFilter(
                                                                       match_type=match_type,
                                                                       value=filter_values,
                                                                       case_sensitive=filter_case
                                                                   )
                                                                   )
                                                     )

        if filter_type == 'in_list_filter':
            self.dimension_filter = FilterExpression(filter=Filter(field_name=field_name,
                                                                   in_list_filter=Filter.InListFilter(
                                                                       values=filter_values,
                                                                       case_sensitive=filter_case
                                                                   )
                                                                   )
                                                     )

        if filter_type == 'numeric_filter':
            self.dimension_filter = FilterExpression(filter=Filter(field_name=field_name,
                                                                   numeric_filter=Filter.NumericFilter(
                                                                       operation=operation,
                                                                       value=filter_values
                                                                       )
                                                                   )
                                                     )

        if filter_type == 'between_filter':
            self.dimension_filter = FilterExpression(filter=Filter(field_name=field_name,
                                                                   between_filter=Filter.BetweenFilter(
                                                                       from_value=from_value,
                                                                       to_value=to_value
                                                                       )
                                                                   )
                                                     )

    def run_report(self) -> pd.DataFrame:
        """
        This is used to actually RunReportRequest, which can be used with add_filter or not

        SAMPLE CODE

        import GA4

        report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

        # add_ filter is optional
        report.add_filter(filter_type='string_filter',
                          field_name='pagePath',
                          match_type=Filter.StringFilter.MatchType.EXACT,
                          filter_values='/Page/1',
                          filter_case=True)

        df = report.run_report()

        :return: pandas.DataFrame
        """
        if self.dimension_filter:
            request = RunReportRequest(property=f'properties/{self.property_id}',
                                       dimensions=self.dimensions,
                                       metrics=self.metrics,
                                       date_ranges=self.date_ranges,
                                       dimension_filter=self.dimension_filter)
        else:
            request = RunReportRequest(property=f'properties/{self.property_id}',
                                       dimensions=self.dimensions,
                                       metrics=self.metrics,
                                       date_ranges=self.date_ranges
                                       )

        # added an extra minute to the timeout
        data = self.client.run_report(request, timeout=3600 * 2)
        # get column names for the metrics and dimensions
        dimension_headers = [header.name for header in data.dimension_headers]
        metric_headers = [header.name for header in data.metric_headers]
        # get row values
        dimension_vals = [val.value for row in data.rows for val in row.dimension_values]
        metric_vals = [val.value for row in data.rows for val in row.metric_values]
        # create your frame
        df = pd.DataFrame(np.transpose([dimension_vals[i::len(self.dimensions)] for i in range(len(self.dimensions))]),
                          columns=dimension_headers)
        # assign metric values
        df.loc[:, metric_headers] = np.transpose([metric_vals[i::len(self.metrics)] for i in range(len(self.metrics))])
        # convert metrics to numeric
        df[df.columns[len(self.dimensions):]] = df[df.columns[len(self.dimensions):]].apply(lambda x: pd.to_numeric(x))
        return df
