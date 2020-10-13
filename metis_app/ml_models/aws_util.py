import os
import boto3

LOCAL_DIRECTORY = 'metis_app/static/'
AWS_ACCESS_KEY_ID = os.environ.get('METIS_APP_AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('METIS_APP_AWS_SECRET_KEY')

if not os.path.exists(LOCAL_DIRECTORY):
    os.mkdir(LOCAL_DIRECTORY)

def aws_download(object_name, local_directory, filename=None,
        bucket_name='metis-projects',
        bucket_directory=None,
    ):

    if bucket_directory:
        object_path = bucket_directory + '/' + object_name
    else:
        object_path = object_name

    if filename:
        download_path =  local_directory + '/' + filename
    else:
        download_path =  local_directory + '/' + object_name

    if not os.path.isfile(download_path):
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
        s3.download_file(bucket_name, object_path, download_path)
    return download_path