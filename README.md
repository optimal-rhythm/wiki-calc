# Wikipedia pageview data pipeline

## Problem Statement

Build a simple application that we can run to compute the top 25 pages on Wikipedia for each of the Wikipedia sub-domains:

- Accept input parameters for the date and hour of data to analyze (default to the current date/hour - 24 hours if not passed, i.e. previous day/hour).
- Download the page view counts from wikipedia for the given date/hour from https://dumps.wikimedia.org/other/pageviews/
- More information on the format can be found here: https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageviews
- Eliminate any pages found in this blacklist: https://s3.amazonaws.com/dd-interview-data/data_engineer/wikipedia/blacklist_domains_and_pages
- Compute the top 25 articles for the given day and hour by total pageviews for each unique domain in the remaining data.
- Save the results to a file, either locally or on S3, sorted by domain and number of pageviews for easy perusal.
- Only run these steps if necessary; that is, not rerun if the work has already been done for the given day and hour.
- Be capable of being run for a range of dates and hours; each hour within the range should have its own result file.

For your solution, explain:

- What additional things would you want to operate this application in a production setting?
- What might change about your solution if this application needed to run automatically for each hour of the day?
- How would you test this application?
- How you’d improve on this application design?

## Setup

This project was built in a Conda environment. To replicate, please follow the steps listed [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

## Running the pipeline

#### Run to get info

```sh
(wiki) $ python app.py -h
usage: app.py [-h] [-st [START_TIME]] [-et [END_TIME]]

Find the top 25 pages for each Wikipedia sub domain

optional arguments:
  -h, --help            show this help message and exit
  -st [START_TIME], --start_time [START_TIME]
                        Start time as MM-DD-YYYY-HH
  -et [END_TIME], --end_time [END_TIME]
                        End time as MM-DD-YYYY-HH

```
#### Run for previous day/hour (default)
```
$ python app.py
```

#### Run for a given hour
```
$ python app.py -s 02-26-2020-09
```

#### Run for a range of hours
```
$ python app.py -s 02-26-2020-09 -e 02-26-2020-12
```

#### What additional things would you want to operate this application in a production setting?
- Certs / Firewall / Ports to be opened
- Use of a robust distributed data store as opposed to local file storage
- Distributed compute if needed & possible
- Logging, monitoring and alerting

#### What might change about your solution if this application needed to run automatically for each hour of the day?
- An event scheduler, could be as simple as cron
- Retries in case of failures

#### How you’d improve on this application design?
- Use distributed compute
- Use Redis or another KV store in place of a Python dict
- Could even consider an in-memory solution instead of reading / writing to disk

#### How would you test this application?
- Basic unit tests can be included
- Can do functional / regression testing with a test harness like PyTest as well
- Can do profiling / performance / stress testing as well though the bottleneck might be the data transfer over the wire