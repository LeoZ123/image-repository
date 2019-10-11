from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
app.config.from_object("img_upload.config")

from .uploadFilesUtils import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "files" not in request.files:
        return "Please select a file!"

    file = request.files.getlist("files")

    permission = request.form['permision']
    if len(file) == 0:
        return "Please select at least one image!"

    if file:
        file_address = upload_img(file, app.config["S3_BUCKET"], permission)
        return json.dumps(file_address)
    else:
        return redirect("/")
