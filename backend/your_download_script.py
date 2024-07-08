import boto3
import os

def download_model_from_s3(bucket_name, model_path, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, model_path, download_path)

bucket_name = 'contentcraftbucket'
model_path = 'models/7B/llama-2-7b-chat.Q4_K_M.gguf'
download_path = './models/7B/llama-2-7b-chat.Q4_K_M.gguf'

if not os.path.exists(download_path):
    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    download_model_from_s3(bucket_name, model_path, download_path)
