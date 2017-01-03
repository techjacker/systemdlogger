from pytest import fixture
from unittest.mock import patch
from systemdlogger.plugin import PluginBase
from systemdlogger.aws import AWSLogger
from systemdlogger.cloudwatch import CloudwatchLogger


@fixture
def init_params():
    return {
        'log_group_name': 'log_group_name',
        'log_stream_name': 'log_stream_name',
        'seq_tok_filename': 'seq_tok_filename',
        'access_key': '1234',
        'secret_key': '567',
        'region': 'eu-west-1'
    }


def test_init(init_params):
    with patch.object(AWSLogger, '__init__') as init:
        with patch.object(CloudwatchLogger, 'setup_logs') as setup_logs:
            cloudwatch_logger = CloudwatchLogger(**init_params)
            assert issubclass(CloudwatchLogger, PluginBase)
            assert isinstance(cloudwatch_logger, PluginBase)
            assert issubclass(CloudwatchLogger, AWSLogger)
            assert isinstance(cloudwatch_logger, AWSLogger)
            init.assert_called_once_with(
                'cloudwatch',
                init_params['access_key'],
                init_params['secret_key'],
                init_params['region']
            )
            setup_logs.assert_called_once_with(
                init_params['seq_tok_filename'],
                init_params['log_group_name'],
                init_params['log_stream_name']
            )
