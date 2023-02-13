# GoogleAnalytics4
A simple python class that takes a list of page paths and returns various dimensions and metrics for each url

First you will need to make sure that you have enabled the Google Analytics Data API v1 in a service account and created a credentials.json. Once you have the credentials.json file, set the path to the file as the following environment variable `GOOGLE_APPLICATION_CREDENTIALS`

You can access additional information by visiting the [Data API quickstart guide](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries)

If you do not want to use an enviorment variable, you can use the optional param `creds_path`, which is the file path to your `credentials.json` file

For example

```
ga = GA4(property_id='123456789', creds_path='/path/to/credentials.json')
```

Below are links to the GA4 Dimensions and Metrics API Names

[GA4 Dimensions](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#dimensions)<br>
[GA4 Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics)

If you have used UA dimensions and metrics in the past, you can review the [Universal Analytics to Google Analytics 4 dimensions and metrics equivalence](https://developers.google.com/analytics/devguides/migration/api/reporting-ua-to-ga4-dims-mets)


# Sample Code

```
from GoogleAnalytics import GA4


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
```
