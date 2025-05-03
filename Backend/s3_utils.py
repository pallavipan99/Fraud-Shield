import boto3
import pandas as pd
from io import StringIO

# Configure AWS S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_REGION'
)

def upload_dataset(df, bucket_name, file_name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())
    print(f"Uploaded {file_name} to S3 bucket {bucket_name}")

def download_dataset(bucket_name, file_name):
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    df = pd.read_csv(response['Body'])
    print(f"Downloaded {file_name} from S3 bucket {bucket_name}")
    return df
