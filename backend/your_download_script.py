import boto3
import os

def download_model_from_s3(bucket_name, model_key, download_path):
    # Fetch AWS credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION')

    # Print statements for debugging
    print(f"AWS Access Key ID: {aws_access_key_id}")
    print(f"Attempting to download model from S3 bucket: {bucket_name}, key: {model_key}, to path: {download_path}")

    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key, 
                      region_name=aws_region)

    # Ensure the directory exists
    directory = os.path.dirname(download_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # Download the file from S3
    s3.download_file(bucket_name, model_key, download_path)
    print(f"Model downloaded from S3 bucket {bucket_name} to {download_path}")
    print(f"Model downloaded to: {download_path}")




