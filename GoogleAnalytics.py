import pandas as pd
import numpy as np
from typing import List
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, FilterExpression, Filter, RunReportRequest


# noinspection PyTypeChecker
class GA4:
    def __init__(self, property_id: str):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()

    def page_path_report(self, page_paths: List[str], ga_metrics: List[str], ga_dimensions: List[str],
                         page_path_case_sensitive: bool, start_date: str, end_date: str) -> pd.DataFrame:
        """
        The page_path_report lets the user list the dimensions and metrics they want for a list of page paths. The
        list of page paths is the "The portion of the URL between the hostname and query string for web pages visited;
        for example, the pagePath portion of https://www.example.com/store/contact-us?query_string=true
        is /store/contact-us."


        Note that the max limit is 100,000
        You can access the list of ga_metrics by visiting
        https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics

        You can access the list of ga_dimensions by visiting
        https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#dimensions

        start_date:
            The inclusive start date for the query in the format
            ``YYYY-MM-DD``. Cannot be after ``end_date``. The format
            ``NdaysAgo``, ``yesterday``, or ``today`` is also accepted,
            and in that case, the date is inferred based on the
            property's reporting time zone.

        end_date:
            The inclusive end date for the query in the format
            ``YYYY-MM-DD``. Cannot be before ``start_date``. The format
            ``NdaysAgo``, ``yesterday``, or ``today`` is also accepted,
            and in that case, the date is inferred based on the
            property's reporting time zone.


        Below is an example script:

        # list of page paths
        page_path_lst = ['/Page/1', '/Page/2', '/Page/3']
        # list of metrics you want to pull for the pages above
        mets = ['screenPageViews', 'activeUsers', 'averageSessionDuration']
        # list of dimensions you want to pull for the above pages
        dims = ['pagePath', 'pageTitle']

        ga = GA4(property_id='123456789')
        df = ga.page_path_report(page_paths=page_path_lst, ga_metrics=mets,
                                 ga_dimensions=dims, page_path_case_sensitive=False,
                                 start_date='2023-02-01', end_date='today')

        :param page_paths: list
        :param ga_metrics: list
        :param ga_dimensions: list
        :param page_path_case_sensitive: bool if the pagePath is case-sensitive or not
        :param start_date: str
        :param end_date: str
        :return: pandas.DataFrame
        """

        request = RunReportRequest(
            property=f'properties/{self.property_id}',
            dimensions=[Dimension(name=x) for x in ga_dimensions],
            metrics=[Metric(name=x) for x in ga_metrics],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=FilterExpression(filter=Filter(field_name='pagePath',
                                                            in_list_filter=Filter.InListFilter(
                                                                values=page_paths,
                                                                case_sensitive=page_path_case_sensitive
                                                            )
                                                            )
                                              )
        )
        # added an extra minute to the timeout
        data = self.client.run_report(request, timeout=3600 * 2)
        # get column names
        dimension_headers = [header.name for header in data.dimension_headers]
        metric_headers = [header.name for header in data.metric_headers]
        # get row values
        dimension_vals = [val.value for row in data.rows for val in row.dimension_values]
        metric_vals = [val.value for row in data.rows for val in row.metric_values]
        # create your frame
        df = pd.DataFrame(np.transpose([dimension_vals[i::len(ga_dimensions)] for i in range(len(ga_dimensions))]),
                          columns=dimension_headers)
        # assign metric values
        df.loc[:, metric_headers] = np.transpose([metric_vals[i::len(ga_metrics)] for i in range(len(ga_metrics))])
        # convert metrics to numeric
        df[df.columns[len(ga_dimensions):]] = df[df.columns[len(ga_dimensions):]].apply(lambda x: pd.to_numeric(x))
        return df



