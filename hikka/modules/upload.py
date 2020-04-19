from werkzeug.datastructures import FileStorage
from hikka.tools.parser import RequestParser
from hikka.decorators import auth_required
from flask import Blueprint, request
from hikka.tools import helpers
from hikka.tools import upload
from hikka.errors import abort

blueprint = Blueprint("upload", __name__)

@blueprint.route("/upload", methods=["PUT"])
@auth_required
def file_upload():
    result = {"error": None, "data": {}}
    choices = ("account", "anime")

    parser = RequestParser()
    parser.argument("subject", type=str, choices=choices, required=True)
    parser.argument("type", type=helpers.string, required=True)
    parser.argument("file", type=FileStorage, location="files")
    parser.argument("uuid", type=helpers.uuid, required=True)
    parser.argument("offset", type=int, required=True)
    parser.argument("index", type=int, required=True)
    parser.argument("total", type=int, required=True)
    parser.argument("size", type=int, required=True)
    parser.argument("slug", type=helpers.string)
    args = parser.parse()

    upload_type = args["type"]
    uuid = args["uuid"]

    if args["subject"] == "account":
        if upload_type not in ("avatar"):
            return abort("file", "bad-upload-type")

        subject = request.account
        folder = subject.username

    if args["subject"] == "anime":
        if upload_type not in ("poster", "banner"):
            return abort("file", "bad-upload-type")

        subject = helpers.anime(args["slug"])
        folder = subject.slug

    chunks = upload.ChunkHelper(request.account, folder, args["file"], upload_type, uuid)
    chunks.load(args["size"], args["index"], args["total"], args["offset"])

    if args["index"] + 1 == args["total"]:
        helper = upload.UploadHelper(request.account, chunks.blob_file, upload_type)

        if args["subject"] == "account":
            file = helper.upload_image()

        if args["subject"] == "anime":
            file = helper.upload_image()

        subject[upload_type] = file
        subject.save()

        result["data"] = subject.dict()
        chunks.clean()

    else:
        result["data"]["chunk"] = True

    return result
