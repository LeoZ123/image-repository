from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config.from_object("img_upload.config")

from .uploadFilesUtils import *

No_FILE_SELECTED = "Please select at least one image!"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "files" not in request.files:
        return No_FILE_SELECTED

    file_list = request.files.getlist("files")

    permission = request.form['permision']
    if len(file_list) == 1 and not file_list[0].filename:
        return No_FILE_SELECTED

    file_address = upload_img(file_list, app.config["S3_BUCKET"], permission)
    
    return json.dumps(file_address)
