import requests
import os
from dotenv import load_dotenv
import boto3
import uuid

load_dotenv()

aws_bucket = os.environ.get("AWS_BUCKET")
aws_region = os.environ.get("AWS_REGION")

def download_image(image_url):
    if image_url is None:
        return None 
    new_filename = uuid.uuid4().hex + ".jpg"
    filename = f"static/images/{new_filename}"
    img_data = requests.get(image_url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    return filename

def upload_file(filename):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY"),
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name = aws_region
    )
    new_filename = uuid.uuid4().hex + ".jpg"
    with open(filename, "rb") as file:
        s3.Bucket(aws_bucket).upload_fileobj(file, new_filename)
    file_url = f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com/{new_filename}"
    os.remove(filename)
    return file_url


