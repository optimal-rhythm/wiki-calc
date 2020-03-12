from datetime import timedelta
import logging

logging.basicConfig(filename='log/trace.log',level=logging.INFO)

class WikiUtils(object):

    def __init__(self, start_time, end_time, counts_dict={}):

        self._start_time = start_time
        self._end_time = end_time
        self._counts_dict = counts_dict
        self._blacklist = self._get_blacklist()
        self._blacklist_count = 0
        self._error_count = 0
        self._total_count = 0

    def _url_generator(self):

        date_format = 'https://dumps.wikimedia.org/other/pageviews/%Y/%Y-%m/pageviews-%Y%m%d-%H0000.gz'
        now = self._start_time
        hour = timedelta(hours=1)
        while now <= self._end_time:
            yield (now, now.strftime(date_format))
            now += hour

    def _count(self, filename_obj):
        with filename_obj.open('r') as file:
            for item in file:
                self._total_count +=1
                try:
                    it = item.split()[:-1]
                    page = (it[0], it[1])
                    count = int(it[-1])
                    self._update_dict(page, count)
                except Exception as e:
                    self._error_count += 1
                    continue
        logging.info('{} lines in blacklist'.format(self._blacklist_count))
        logging.info('{} lines caused an error'.format(self._error_count))
        logging.info('{} lines read'.format(self._total_count))

    def _update_dict(self, page, view):
        if page in self._blacklist:
            self._blacklist_count +=1
            return
        if page in self._counts_dict:
            self._counts_dict[page] += int(view)
        else:
            self._counts_dict[page] = int(view)

    @staticmethod
    def _get_blacklist():
        with open('resources/blacklist_domains_and_pages') as file:
            blacklist = set(tuple(item.rstrip().split(' ')) for item in file)
        return blacklist