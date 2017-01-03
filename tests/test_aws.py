import pytest
from unittest.mock import patch
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


class TestInit:

    @pytest.mark.parametrize(('backend'), allowed_services)
    def test_init(self, backend, aws_params):
        with patch.object(AWSLogger, 'load_metadata') as load_metadata:
            with patch.object(AWSLogger, 'create_client') as create_client:
                aws = AWSLogger(backend, **aws_params)
                assert aws.aws_service == backend
                create_client.assert_called_once_with(**aws_params)
                assert load_metadata.call_count == 1

    @pytest.mark.parametrize(('backend'), allowed_services)
    def test_init_aws(self, backend, aws_params, metadata):
        with patch.object(AWSLogger, 'load_metadata') as load_metadata:
            load_metadata.returns = metadata
            logger = AWSLogger(backend, **aws_params)
            assert isinstance(
                logger.client, botocore.client.BaseClient)
