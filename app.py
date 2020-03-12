from sys import path
path.append("src/main/python")

import arg_parser
import luigi
import tasks
import datetime,logging

logging.basicConfig(filename='log/trace.log',level=logging.INFO)
parser = arg_parser.ArgParser()
args = parser._run()
logging.info('Computing from {} to {}'.format(args.start_time.strftime('%d %b %Y %H'), args.end_time.strftime('%d %b %Y %H')))
now = datetime.datetime.now()
luigi.build([tasks.FindAllTopPages(start_time=args.start_time, end_time=args.end_time)], local_scheduler=True,log_level='INFO')
logging.info('Completed in {}s'.format((datetime.datetime.now()-now).total_seconds()))