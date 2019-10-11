import boto3
from img_upload import app
from botocore.client import Config

ALLOWED_IMG_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"],
    config=Config(signature_version='s3v4')
)

def is_img_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_IMG_TYPES

def upload_img(files, bucket_name, acl="public-read"):
    try:
        url_list = []
        for file in files:      
            if is_img_file(file.filename):
                s3.upload_fileobj(
                    file,
                    bucket_name,
                    file.filename,
                    ExtraArgs={
                        "ACL": acl,
                        "ContentType": file.content_type
                    }
                )
                file_url = "{}{}".format(app.config["S3_LOCATION"],file.filename)
                url_list.append(file_url)
        return url_list
    except Exception as e:
        print("EROOR:: ", e)
        return e
