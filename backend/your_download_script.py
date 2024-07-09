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

    # Ensure the parent directory exists
    directory = os.path.dirname(download_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # Temporary path for download to avoid conflicts
    temp_download_path = download_path + ".temp"
    
    try:
        # Download the file from S3
        s3.download_file(bucket_name, model_key, temp_download_path)
        # Rename the temporary file to the desired path
        os.rename(temp_download_path, download_path)
        print(f"Model downloaded from S3 bucket {bucket_name} to {download_path}")
    except Exception as e:
        print(f"Error downloading the model: {e}")
        # Clean up temporary file in case of failure
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)
        raise

# Define your S3 bucket name, model key, and download path
bucket_name = 'contentcraftbucket'
model_key = 'models/7B/llama-2-7b-chat.Q4_K_M.gguf'
download_path = './models/7B/llama-2-7b-chat.Q4_K_M.gguf'

# Call the download function
download_model_from_s3(bucket_name, model_key, download_path)
