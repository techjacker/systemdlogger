# from pytest import fixture
import pytest
from unittest.mock import Mock
from systemdlogger.plugin import PluginBase
from systemdlogger.aws import AWSLogger
from systemdlogger.cloudwatch import CloudwatchLogger


def params():
    return {
        'log_group_name': 'log_group_name',
        'log_stream_name': 'log_stream_name',
        'seq_tok_filepath': 'seq_tok_filepath',
    }


def params_with_aws():
    p = params()
    p['aws_params'] = {
        'access_key': '1234',
        'secret_key': '567',
        'region': 'eu-west-1'
    }
    return p


@pytest.mark.parametrize(('init_params'), [
    params(),
    params_with_aws()
])
class TestInitCloudwatch:
    def setup_method(self, method):
        self.AWSLogger = AWSLogger
        self.AWSLogger.__init__ = Mock()
        self.CloudwatchLogger = CloudwatchLogger
        self.CloudwatchLogger.setup_logs = Mock()

    def teardown_method(self, method):
        self.AWSLogger.__init__.restore()
        self.CloudwatchLogger.setup_logs.restore()

    def test_init(self, init_params):
        cloudwatch_logger = CloudwatchLogger(**init_params)
        assert issubclass(CloudwatchLogger, PluginBase)
        assert isinstance(cloudwatch_logger, PluginBase)
        assert issubclass(CloudwatchLogger, AWSLogger)
        assert isinstance(cloudwatch_logger, AWSLogger)
        self.AWSLogger.__init__.assert_called_once_with(
            'logs',
            init_params.get('aws_params', {})
        )
        self.CloudwatchLogger.setup_logs.assert_called_once_with(
            init_params['seq_tok_filepath'],
            init_params['log_group_name'],
            init_params['log_stream_name']
        )
