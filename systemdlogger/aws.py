import requests
import boto3
from boto3.session import Session
from systemdlogger.log import log


class AWSLogger():

    services = ['cloudwatch']
    metadata_url = (
        'http://169.254.169.254'
        '/latest/dynamic/instance-identity/document'
    )

    # def __init__(self, aws_service, access_key, secret_key, region):
    def __init__(self, aws_service, aws_params={}):
        if aws_service not in AWSLogger.services:
            raise Exception('logger must be one of %s' % AWSLogger.services)
        self.aws_service = aws_service
        self.metadata = self.load_metadata()
        self.client = self.create_client(**aws_params)

    def create_client(self, access_key, secret_key, region):
        if access_key and secret_key and region:
                self.session = self.create_session(
                    access_key=access_key,
                    secret_key=secret_key,
                    region=region
                )
                return self.session.client(self.aws_service)
        else:
            return boto3.client(
                self.aws_service,
                region_name=self.metadata['region']
            )

    def create_session(self, access_key, secret_key, region):
        return Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def load_metadata(self):
        try:
            response = requests.get(AWSLogger.metadata_url)
            return response.json()
        # assume we are testing locally if not on ec2
        except Exception as e:
            log('Not on AWS', e)
            return {}

    def get_instance_id(self):
        return self.metadata['instanceId'] \
            if 'instanceId' in self.metadata \
            else 'test-instance-id'
