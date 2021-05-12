import unittest
import boto3
from moto import mock_s3


class TestConnectors(unittest.TestCase):

    @mock_s3
    def test_awss3connector(self):
        """
            test s3 connection
        """
        from core.connectors.awss3.client import AwsS3Client
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='mybucket')

        aws_s3 = AwsS3Client()
        aws_s3.authenticate(
            aws_access_key_id='aws_access_key_id',
            aws_secret_access_key='aws_secret_access_key',
            bucket_name='mybucket',
            aws_region='us-east-1'
        )

    # def test_salesforceconnector(self):
    #     """
    #         Test salesforce connector
    #     """

# if __name__ == '__main__':
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestConnectors)
#     result = unittest.TextTestRunner(verbosity=2, buffer=True).run(suite)
