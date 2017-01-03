import os
import errno
import botocore
from systemdlogger.plugin import PluginBase
from systemdlogger.aws import AWSLogger
from systemdlogger.log import log


class CloudwatchLogger(AWSLogger, PluginBase):
    def __init__(
        self,
        seq_tok_filepath,
        log_group_name,
        log_stream_name,
        aws_params={}
    ):
        super().__init__('cloudwatch', aws_params)
        self.setup_logs(seq_tok_filepath, log_group_name, log_stream_name)

    def setup_logs(self, seq_tok_filepath, log_group_name, log_stream_name):
        self.seq_token_path = self.set_seq_token_path(
            seq_tok_filepath, log_group_name, log_stream_name)
        self.instance_id = self.get_instance_id()
        self.log_group_name = log_group_name
        self.log_stream_name = '%s-%s' % (log_stream_name, self.instance_id)
        # self.log_group_name = '%s-%s' % (project, env)
        # self.log_stream_name = '%s-%s' % (app, self.instance_id)

        try:
            self.client.create_log_group(logGroupName=self.log_group_name)
        except botocore.exceptions.ClientError:
            pass

        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name
            )
        except botocore.exceptions.ClientError:
            pass

    @staticmethod
    def set_seq_token_path(filepath, log_group_name, log_stream_name):
        return filepath if filepath else os.path.join(
            os.getcwd(),
            'aws_seq_tok-%s-%s.txt' % (log_group_name, log_stream_name)
        )

    def get_last_token(self):
        try:
            with open(self.seq_token_path, 'r') as store:
                contents = store.read().strip()
                log('contents', contents)
                return contents if contents else '0'
        except OSError as e:
            # okay if file doesn't exist yet (must be brand new log stream)
            if e.errno == errno.ENOENT:
                pass
            else:
                log('get_last_token_error', e)

        # must be brand new log stream
        return '0'

    def set_last_token(self, token):
        log('token', token)
        with open(self.seq_token_path, 'w') as store:
            store.write(token)

    def create_payload(self, entries):
        return [{
            # AWS wants time in milliseconds
            'timestamp': int(entry['__REALTIME_TIMESTAMP'].timestamp()) * 1000,
            'message': str(entry['MESSAGE'])
        } for entry in entries]

    # data = [
    #     {
    #         'timestamp': int(time.time()) * 1000,
    #         'message': 'fourth'
    #     }
    # ]
    def save(self, data):
        token = self.get_last_token()
        log('AWS token: ', token)
        response = self.client.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=self.log_stream_name,
            logEvents=self.create_payload(data),
            sequenceToken=token
        )
        log('response', response)
        return response
