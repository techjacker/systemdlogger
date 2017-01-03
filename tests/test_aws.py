import pytest
from unittest.mock import patch, Mock
from systemdlogger.aws import AWSLogger
import botocore


@pytest.fixture
def aws_params():
    return {
        'access_key': '1234',
        'secret_key': '567',
        'region': 'eu-west-1'
    }


@pytest.fixture
def metadata():
    return {
        'region': 'eu-west-1',
        'instanceId': 1234
    }


allowed_services = [
    'cloudwatch'
]


@pytest.mark.parametrize(('backend'), allowed_services)
class TestInit:

    def setup_method(self, method):
        self.AWSLogger = AWSLogger
        self.AWSLogger.load_metadata = Mock(return_value=metadata())

    def teardown_method(self, method):
        self.AWSLogger.load_metadata.restore()

    def test_init_load_metadata(self, backend, aws_params):
        with patch.object(self.AWSLogger, 'create_client') as create_client:
            aws = self.AWSLogger(backend, **aws_params)
            assert aws.aws_service == backend
            create_client.assert_called_once_with(**aws_params)
            assert self.AWSLogger.load_metadata.call_count == 1

    def test_init_create_client(self, backend, aws_params, metadata):
        logger = self.AWSLogger(backend, **aws_params)
        assert isinstance(
            logger.client, botocore.client.BaseClient)
