import boto3
import os

def download_model_from_s3(bucket_name, model_key, download_path):
    s3 = boto3.client('s3')
    directory = os.path.dirname(download_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    if not os.path.exists(download_path):
        print(f"Downloading {model_key} from {bucket_name} to {download_path}")
        s3.download_file(bucket_name, model_key, download_path)
        print(f"Model downloaded to {download_path}")
    else:
        print(f"Model already exists at {download_path}")
