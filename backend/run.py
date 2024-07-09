import os
from app import create_app
from your_download_script import download_model_from_s3

# Download model from S3 during startup
bucket_name = 'contentcraftbucket'
model_key = 'models/7B/llama-2-7b-chat.Q4_K_M.gguf'
download_path = './models/7B/llama-2-7b-chat.Q4_K_M.gguf'

# Ensure the model is downloaded
download_model_from_s3(bucket_name, model_key, download_path)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
