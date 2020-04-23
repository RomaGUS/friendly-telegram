from werkzeug.datastructures import FileStorage
from hikka.services.anime import AnimeService
from hikka.services.files import FileService
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
    choices = ("account", "anime", "episode")

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
    parser.argument("position", type=int)
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

    if args["subject"] == "episode":
        if upload_type not in ("video", "thumbnail"):
            return abort("file", "bad-upload-type")

        subject = helpers.anime(args["slug"])
        index = AnimeService.position_index(subject, args["position"])
        if index is None:
            return abort("episode", "not-found")

        folder = subject.slug + "/" + str(args["position"])

    chunks = upload.ChunkHelper(request.account, folder, args["file"], upload_type, uuid)
    chunks.load(args["size"], args["index"], args["total"], args["offset"])

    if args["index"] + 1 == args["total"]:
        helper = upload.UploadHelper(request.account, chunks.blob_file, upload_type)

        if args["subject"] in ("account", "anime"):
            file = helper.upload_image()
            FileService.destroy(subject[upload_type])
            subject[upload_type] = file

        if args["subject"] == "episode":
            if upload_type == "video":
                file = helper.upload_video()

            else:
                file = helper.upload_image()

            FileService.destroy(subject.episodes[index][upload_type])
            subject.episodes[index][upload_type] = file

        subject.save()
        result["data"] = subject.dict()
        chunks.clean(True)

    else:
        result["data"]["chunk"] = True

    return result
