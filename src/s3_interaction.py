import boto3
import logging
from botocore.exceptions import ClientError


class S3Interactor:
    def __init__(self):
        # Add your secret and access keys and endpoint address obtained from arvan cloud:
        secret_key = ""
        access_key = ""
        endpoint = ""
        try:
            self.s3_resource = boto3.resource(
                "s3",
                endpoint_url=endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            self.bucket = self.s3_resource.Bucket("iamabucket")
        except Exception as exc:
            logging.error(exc)

    def upload_file(self, file, file_key):
        try:
            self.bucket.put_object(
                ACL="private",
                Body=file,
                Key=file_key
            )
        except ClientError as e:
            logging.error(e)


    def download_file(self, download_path, file_key):
        try:
            self.bucket.download_file(
                file_key,
                download_path
            )
        except ClientError as e:
            logging.error(e)
