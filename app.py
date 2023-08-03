from cgitb import text
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.datastructures import FileStorage
from tract import extract_text_from_image
from io import BytesIO
from shutil import copyfileobj
import json


app = Flask(__name__)
api = Api(app)

# resources = {r"*": {"origins": "*"}}
# CORS(app, resources=resources, max_age=216000)

app.static_folder = 'static'
app.static_url_path = '/static'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Html(Resource):
    def get(self):
        return app.send_static_file('index.html')


class Healthy(Resource):
    def get(self):
        return "hello", 200


class UploadImage(Resource):
    def post(self):
        if 'image' not in request.files:
            return {'message': 'No image part in the request'}, 400

        image_file = request.files['image']

        # 检查是否有文件名和文件类型
        if image_file.filename == '':
            return {'message': 'No selected image'}, 400

        if image_file and allowed_file(image_file.filename):
            filename = image_file.filename
            a = FileStorage(image_file)
            byte_stream = BytesIO()
            copyfileobj(a.stream, byte_stream)
            image_bytes = byte_stream.getvalue()
            txt = extract_text_from_image(image_bytes)[0:1]
            return jsonify(txt)
        else:
            return {'message': 'Allowed image types are png, jpg, jpeg, gif'}, 400


def allowed_file(filename):
    # 允许上传的图片类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


api.add_resource(UploadImage, '/upload')
api.add_resource(Healthy, '/ping')
api.add_resource(Html, '/')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5016)
