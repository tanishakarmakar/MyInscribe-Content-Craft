import boto3
import os

def download_model_from_s3(bucket_name, model_key, download_path):
    s3 = boto3.client('s3')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    
    # Download the file from S3
    s3.download_file(bucket_name, model_key, download_path)
    print(f"Model downloaded to: {download_path}")




