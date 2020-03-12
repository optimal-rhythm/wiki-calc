import argparse
import datetime
from datetime import timedelta

class ArgParser(object):

    def __init__(self):
        self._parser = self._create()

    def validate_time(self, date_time):
        try:
            return datetime.datetime.strptime(date_time, '%m-%d-%Y-%H')
        except ValueError:
            msg = "Invalid date: '{0}'.".format(date_time)
            raise argparse.ArgumentTypeError(msg)

    def _create(self):
        parser = argparse.ArgumentParser(description='Find the top 25 pages for each Wikipedia sub domain')
        parser.add_argument("-st",
                            "--start_time",
                            help="Start time as MM-DD-YYYY-HH",
                            nargs='?',
                            type=self.validate_time,
                            default=datetime.datetime.now() - timedelta(hours=24))
        parser.add_argument("-et",
                            "--end_time",
                            help="End time as MM-DD-YYYY-HH",
                            nargs='?',
                            type=self.validate_time)
        return parser

    def _run(self):
        args = self._parser.parse_args()
        args.end_time = args.start_time if args.end_time is None else args.end_time
        return args