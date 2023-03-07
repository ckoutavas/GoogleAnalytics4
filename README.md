# Google Analytics 4 Data API Python Wrapper
## Cloning the Repo and Setup
1. Create a virtual environment: `conda create -n py_ga4 python=3.10`
2. Change the dirctory to your site-packages: `cd /Users/ckoutavas/opt/anaconda3/envs/py_ga4/lib/python3.10/site-packages`
3. Clone the repo: `git clone https://github.com/ckoutavas/GoogleAnalytics4`
4. Change the directory to GoogleAnalytics4: `cd GoogleAnalytics4`
5. Activate your new enviorment: `conda activate py_ga4`
6. Install requirements.txt: `pip install -r requirements.txt`

After you clone the repo, make sure that you have enabled the Google Analytics Data API v1 in a service account and created a credentials.json. Once you have the credentials.json file, set the path as the following environment variable `GOOGLE_APPLICATION_CREDENTIALS`

 - [Python client install guide](https://github.com/googleapis/python-analytics-data#installation)
 - [Data API quickstart guide](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries)

If you do not want to use an enviorment variable, you can use the optional param `creds_path`, which is the file path to your `credentials.json` file

```
from GoogleAnalytics4 import GA4


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today',
                         creds_path='/path/to/credentials.json')
```

Below are links to the GA4 dimensions and metrics API names:

 - [GA4 Dimensions](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#dimensions)
 - [GA4 Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics)

If you have used UA dimensions and metrics in the past, you can review the [Universal Analytics to Google Analytics 4 dimensions and metrics equivalence](https://developers.google.com/analytics/devguides/migration/api/reporting-ua-to-ga4-dims-mets)

## No Filter

```
from GoogleAnalytics4 import GA4


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

df = report.run_report()

```

## string_filter

The match type of a string filter:
 - MATCH_TYPE_UNSPECIFIED = 0
 - EXACT = 1
 - BEGINS_WITH = 2
 - ENDS_WITH = 3
 - CONTAINS = 4
 - FULL_REGEXP = 5
 - PARTIAL_REGEXP = 6
 
 The match type can be added using: 
  - `Filter.StringFilter.MatchType.EXACT`
  - `Filter.StringFilter.MatchType(1)`

```
from GoogleAnalytics4 import GA4
from google.analytics.data_v1beta.types import Filter


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

report.add_filter(filter_type='string_filter',
                  filter_dimension=True,
                  field_name='pagePath',
                  match_type=Filter.StringFilter.MatchType.EXACT,
                  filter_values='/Page/1',
                  filter_case=True)

df = report.run_report()

```

## in_list_filter

```
from GoogleAnalytics4 import GA4


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

report.add_filter(filter_type='in_list_filter',
                  filter_dimension=True,
                  field_name='pagePath',
                  filter_values=['/', '/Page/1', '/Page/2'],
                  filter_case=False)

df = report.run_report()

```

## numeric_filter

The operation applied to a numeric filter:
 - OPERATION_UNSPECIFIED = 0
 - EQUAL = 1
 - LESS_THAN = 2
 - LESS_THAN_OR_EQUAL = 3
 - GREATER_THAN = 4
 - GREATER_THAN_OR_EQUAL = 5
 
 The operation can be added using:
  - `Filter.NumericFilter.Operation.GREATER_THAN_OR_EQUAL`
  - `Filter.NumericFilter.Operation(5)`

```
from GoogleAnalytics4 import GA4
from google.analytics.data_v1beta.types import Filter, NumericValue


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

report.add_filter(filter_type='numeric_filter',
                  filter_dimension=True,
                  field_name='dayOfWeek',
                  operation=Filter.NumericFilter.Operation.GREATER_THAN_OR_EQUAL,
                  filter_values=NumericValue({'int64_value': '5'}))

df = report.run_report()

```

## between_filter
Can only be used with a [GA4 Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics), not dimensions

```
from GoogleAnalytics4 import GA4
from google.analytics.data_v1beta.types import Filter, NumericValue


report = GA4.BuildReport(property_id='123456789',
                         ga_dimensions=['pagePath', 'pageTitle'],
                         ga_metrics=['screenPageViews', 'activeUsers', 'averageSessionDuration'],
                         start_date='2023-02-01',
                         end_date='today')

report.add_filter(filter_type='between_filter',
                  filter_dimension=False,
                  field_name='screenPageViews',
                  from_value=NumericValue({'int64_value': '100'}),
                  to_value=NumericValue({'int64_value': '200'}))

df = report.run_report()
```
