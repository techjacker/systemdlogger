from systemdlogger.log import log
from systemdlogger.journal import JournalExporter
from systemdlogger.cloudwatch import CloudwatchLogger
from systemdlogger.elasticsearch import ElasticsearchLogger
import json


class Runner:
    loggers = {
        'cloudwatch': CloudwatchLogger,
        'elasticsearch': ElasticsearchLogger
    }

    def __init__(
        self,
        config_path
    ):
        config = self.load_config(config_path)

        self.journal = JournalExporter(**config['systemd'])

        if len(config['backends']):
            self.loggers = [
                Runner.loggers[backend](**config['backends'][backend])
                for backend in config['backends']
            ]

    @staticmethod
    def load_config(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)

    def save(self, entries):

        for logger in self.loggers:
            res = logger.save(entries)

            # verify cloudwatch logger succeeded
            if isinstance(logger, CloudwatchLogger):
                if 'nextSequenceToken' in res:
                    logger.set_last_token(res['nextSequenceToken'])
                else:
                    print('did not write to logger successfully')
                    raise

    def run(self):
        try:
            entries = self.journal.get_entries()
            if entries:
                self.save(entries)
                # if all backends succeed
                self.journal.set_cursor(entries)
            else:
                print('no new entries')
        except Exception as e:
            log('e', e)
            raise
