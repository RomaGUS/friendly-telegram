from werkzeug.datastructures import FileStorage
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from hikka.tools.upload import get_size
from flask import Blueprint, request
from hikka.tools import helpers
from hikka.errors import abort
import shutil
import os

blueprint = Blueprint("upload", __name__)

@blueprint.route("/upload", methods=["PUT"])
@auth_required
def file_upload():
    result = {"error": None, "data": {}}
    choices = ("poster", "banner")

    parser = RequestParser()
    parser.argument("type", type=str, choices=choices, required=True)
    parser.argument("file", type=FileStorage, location="files")
    parser.argument("uuid", type=helpers.uuid, required=True)
    parser.argument("offset", type=int, required=True)
    parser.argument("index", type=int, required=True)
    parser.argument("total", type=int, required=True)
    parser.argument("size", type=int, required=True)
    args = parser.parse()

    file = args["file"]
    offset = args["offset"]
    folder = request.account.username
    upload_type = args["type"]
    size = get_size(file)
    uuid = args["uuid"]

    if args["size"] != size:
        return abort("file", "invalid-size")

    tmp_dir = f"/tmp/hikka/{folder}/{upload_type}/"
    uuid_dir = os.path.join(tmp_dir, uuid)

    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_ls = os.listdir(tmp_dir)

    if uuid not in tmp_ls:
        shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)
        os.mkdir(uuid_dir)

    blob_file = os.path.join(uuid_dir, "blob")

    with open(blob_file, "ab") as blob:
        blob.seek(offset)
        blob.write(file.stream.read())

    result["data"]["ls"] = os.listdir(tmp_dir)

    return result
