import io
import gzip
import os
import luigi
import pandas as pd
import requests
import logging
from io import BytesIO
from wiki_utils import *
from datetime import datetime

logging.basicConfig(filename='log/trace.log',level=logging.INFO)

class GetHourlyData(luigi.Task):

    url = luigi.Parameter()

    def run(self):
        logging.info('Geting Hour Data for {}'.format(datetime.strptime(self.url.split('/')[-1],'pageviews-%Y%m%d-%H0000.gz')))
        data = requests.get(self.url, stream=True)
        gzFile = BytesIO(data.content)
        textFile = gzip.GzipFile(fileobj=gzFile, mode='rw')
        with self.output().open('w') as hour_data:
            hour_data.write(textFile.read().decode('utf-8'))
        logging.info('Got data successfully')

    def output(self):
        return luigi.LocalTarget("work_dir/" + self.url.split('/')[-1].replace('.gz', '.txt'))

class FindTopPages(luigi.Task):

    dt = luigi.DateHourParameter()
    file = luigi.Parameter()
    
    def requires(self):
        return GetHourlyData(self.file)

    def run(self):
        logging.info('Getting top 25 for {}'.format(self.dt))
        wiki_util = WikiUtils(self.dt, self.dt)
        wiki_util._count(self.input())
        mi = pd.MultiIndex.from_tuples(
            wiki_util._counts_dict.keys(), names=['Domain', 'Page'])
        df = pd.DataFrame(wiki_util._counts_dict.values(), index=mi, columns=['Count'])
        mi = None
        df.groupby(level=0)['Count'].nlargest(25).to_csv(self.output().path)
        logging.info('Done')

    def output(self):
        return luigi.LocalTarget('output/' + self.dt.strftime('%m-%d-%Y-%H') + "_" + self.dt.strftime('%m-%d-%Y-%H') + ".csv")

    def on_success(self):
        os.remove(self.input().path)

class FindAllTopPages(luigi.Task):

    start_time = luigi.DateHourParameter()
    end_time = luigi.DateHourParameter()
    
    def requires(self):
        wiki_util = WikiUtils(self.start_time, self.end_time)
        return [FindTopPages(dt, file) for dt, file in wiki_util._url_generator()]

    def run(self):
        logging.info('Top 25 computation complete')
        self.output().open('w').close()

    def output(self):
        return luigi.LocalTarget('',is_tmp=True)