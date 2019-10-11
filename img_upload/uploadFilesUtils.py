import boto3
import time
from img_upload import app
from botocore.client import Config

ALLOWED_IMG_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_S3_PERMISSIONS = set(['public-read', 'private'])

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"],
    config=Config(signature_version='s3v4')
)

def is_img_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_IMG_TYPES

def is_valid_permission(acl):
    return acl in ALLOWED_S3_PERMISSIONS

def formate_file_name(name):
    ts = str(time.time())
    file_name = name.split(".")[0].lower() + '_' + ts + '.' + name.split(".")[1].lower()
    return file_name

def upload_img(files, bucket_name, acl="public-read"):
    try:
        url_list = []
        for file in files:    
            file_name = file.filename
            if is_img_file(file_name) and is_valid_permission(acl):
                formatted_file_name = formate_file_name(file_name)
                s3.upload_fileobj(
                    file,
                    bucket_name,
                    formatted_file_name,
                    ExtraArgs={
                        "ACL": acl,
                        "ContentType": file.content_type
                    }
                )
                file_url = "{}{}".format(app.config["S3_LOCATION"], formatted_file_name)
                url_list.append([file_name, file_url])
        return url_list
    except Exception as e:
        print("EROOR:: ", e)
        return e
