# Google Analytics 4 Data API - Python
First you will need to make sure that you have enabled the Google Analytics Data API v1 in a service account and created a credentials.json. Once you have the credentials.json file, set the path to the file as the following environment variable `GOOGLE_APPLICATION_CREDENTIALS`

You can access additional information by visiting the [Data API quickstart guide](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries)

If you do not want to use an enviorment variable, you can use the optional param `creds_path`, which is the file path to your `credentials.json` file

For example

```
import GA4


report = GA4.BuildReport(property_id='12345678',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today',
                         creds_path='/path/to/credentials.json')
```

Below are links to the GA4 Dimensions and Metrics API Names

[GA4 Dimensions](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#dimensions)<br>
[GA4 Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics)

If you have used UA dimensions and metrics in the past, you can review the [Universal Analytics to Google Analytics 4 dimensions and metrics equivalence](https://developers.google.com/analytics/devguides/migration/api/reporting-ua-to-ga4-dims-mets)


# No Filter

```
import GA4


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

df = report.run_report()

```

# string_filter

```
import GA4
from google.analytics.data_v1beta.types import Filter


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

df = report.run_report()

```

# in_list_filter

```
import GA4


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

report.add_filter(filter_type='in_list_filter',
                  field_name='pagePath',
                  filter_values=['/Page/1', '/Page/2', '/Page/3'],
                  filter_case=False)

df = report.run_report()

```

# numeric_filter

```
import GA4
from google.analytics.data_v1beta.types import Filter, NumericValue


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

report.add_filter(filter_type='numeric_filter',
                  field_name='day',
                  operation=Filter.NumericFilter.Operation.GREATER_THAN_OR_EQUAL,
                  filter_values=NumericValue({'int64_value': '10'}))

df = report.run_report()

```

# between_filter
There appears to be a bug with `Filter.BetweenFilter` - [GH Issue 342](https://github.com/googleapis/python-analytics-data/issues/342)
