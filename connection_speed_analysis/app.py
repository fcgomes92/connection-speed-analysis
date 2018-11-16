import sys

import argparse
import csv
import os
import speedtest
from crontab import CronTab

DIRNAME = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(DIRNAME)


class SpeedAnalysis(object):
    _parser = None
    _args = {}
    _RESULTS_PATH = os.path.join(os.environ['HOME'], '.connection_speed_analysis')

    def __init__(self):
        self.prepare_parsers()
        self._args = vars(self._parser.parse_args())
        command = self._args.pop('command', None)

        if not command:
            self._parser.print_help()
            exit(1)

        command(**self._args)

    def _flat_dict(self, value, key=None):
        d = {}
        for k, v in value.items():
            if isinstance(v, dict):
                d = {**d, **self._flat_dict(v, key=k)}
            else:
                if key:
                    d[f'{key}_{k}'] = v
                else:
                    d[k] = v
        return d

    def _to_mbytes(self, value):
        return value / 8e+6

    def _save_result_to_csv(self, result):
        result_file = os.path.join(self._RESULTS_PATH, 'results.csv')

        result_dict = self._flat_dict(result)
        result_dict['download'] = self._to_mbytes(result_dict['download'])
        result_dict['upload'] = self._to_mbytes(result_dict['upload'])

        headers = result_dict.keys()

        if not os.path.exists(self._RESULTS_PATH):
            os.makedirs(self._RESULTS_PATH, exist_ok=True, mode=0o770)
        writer_header = not os.path.exists(result_file)

        with open(result_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';',
                                    quotechar='"',
                                    fieldnames=headers,
                                    quoting=csv.QUOTE_MINIMAL)
            if writer_header:
                writer.writeheader()
            writer.writerow(result_dict)

    def prepare_parsers(self):
        self._parser = argparse.ArgumentParser(description='Speed Analysis CLI')
        subparsers = self._parser.add_subparsers()

        set_cron_parser = subparsers.add_parser('test_speed')
        set_cron_parser.set_defaults(command=self.test_speed)

        set_cron_parser = subparsers.add_parser('set_cron')
        set_cron_parser.add_argument('cron')
        set_cron_parser.set_defaults(command=self.set_cron)

    def set_cron(self, **kwargs):
        cron = CronTab(user=True)
        comment = '_connection_speed_analysis_command'
        job = cron.find_comment(comment)
        if job:
            cron.remove(job)
        job = cron.new(command=kwargs['cron'], comment=comment)
        job.setall('0 * * * *')
        cron.write()

    def test_speed(self, **_):
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        s.results.share()
        self._save_result_to_csv(s.results.dict())


def main():
    try:
        SpeedAnalysis()
    except KeyboardInterrupt:
        print('So Long, and Thanks for All the Fish!')


if __name__ == '__main__':
    main()
