from flask_restful import Resource
from flask import request
from hikka import utils
from hikka import api
import os

class Upload(Resource):
    def post(self):
        if "upload" in request.files:
            # hls = Hls("hikka/konosuba/hls/")
            # Return True here and start processing video in separate thread
            # hls.ffmpeg()
            # hls.process()

            # ToDo: support different file types
            # Only mp4 for now
            file = request.files["upload"]
            if file.mimetype in ["video/mp4"]:
                name = utils.pebble()
                tmp_dir = f"/tmp/hikka-{name}/"
                tmp_file = tmp_dir + f"{name}.mp4"

                if not os.path.exists(tmp_dir):
                    os.makedirs(tmp_dir)

                with open(tmp_file, "wb") as file_local:
                    file_local.write(file.read())

                return True

            return False
        else:
            return False


api.add_resource(Upload, "/api/upload")
