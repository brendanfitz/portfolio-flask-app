from os import path, environ, makedirs
import boto3

class S3Downloader(object):
    BUCKET_NAME = 'metis-projects'
    AWS_CREDS = dict(
        aws_access_key_id=environ.get('PORTFOLIO_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=environ.get('PORTFOLIO_AWS_SECRET_KEY'),
    )
    
    def __init__(self, local_dir):
        self.local_dir = local_dir

        if not path.exists(self.local_dir):
            makedirs(self.local_dir)

    
    def download(self, obj_name, filename=None, bucket_dir=None):
        obj_path = bucket_dir + '/' + obj_name if bucket_dir else obj_name

        download_path = path.join(self.local_dir, (filename or obj_name))
    
        if not path.isfile(download_path):
            s3 = boto3.client('s3', **S3Downloader.AWS_CREDS)
            s3.download_file(S3Downloader.BUCKET_NAME, obj_path, download_path)
        return download_path