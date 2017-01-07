import requests
import boto3
from boto3.session import Session
from systemdlogger.log import log


class AWSDefaults():

    SERVICES = ['logs']
    METADATA_URL = (
        'http://169.254.169.254'
        '/latest/dynamic/instance-identity/document'
    )
    CREDS = {
        'access_key': '',
        'secret_key': '',
        'region': ''
    }


class AWSLogger(AWSDefaults):

    def __init__(self, aws_service, aws_params=AWSDefaults.CREDS):
        if aws_service not in AWSDefaults.SERVICES:
            raise Exception(
                'logger must be one of %s'.format(AWSDefaults.SERVICES)
            )
        self.aws_service = aws_service
        self.metadata = self.load_metadata()
        self.client = self.create_client(**aws_params)

    def create_client(
        self,
        access_key=AWSDefaults.CREDS['access_key'],
        secret_key=AWSDefaults.CREDS['secret_key'],
        region=AWSDefaults.CREDS['region']
    ):
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
            response = requests.get(AWSDefaults.METADATA_URL)
            return response.json()
        # assume we are testing locally if not on ec2
        except Exception as e:
            log('Not on AWS', e)
            return {}

    def get_instance_id(self):
        return self.metadata['instanceId'] \
            if 'instanceId' in self.metadata \
            else 'test-instance-id'
