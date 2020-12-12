import os
import uuid
import mimetypes
import io
from celery.result import AsyncResult
from flask import Flask, Blueprint, Response, flash, request, redirect, send_file, abort
from flask_restplus import Api, Resource, fields
from tasks import predict, storage_folder
from tasks import app as celery_app
from parsers import file_upload

app = Flask(__name__, static_url_path='/static')
api = Api(version='1.0')

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
app.register_blueprint(blueprint)


@api.route('/predict')
class Predict(Resource):
    task_model = api.model('Task', {
        'task_id': fields.String,
        'filename': fields.String
    })

    @api.response(200, 'Task enqueued successfully', task_model)
    @api.expect(file_upload)
    def post(self):
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        filename = '{uuid}{extension}'.format(
                uuid=str(uuid.uuid4()),
                extension=os.path.splitext(file.filename)[1]
            )
        file.save(os.path.join(storage_folder, filename))

        task = predict.apply_async(routing_key='predict',
                                   kwargs={'filename': filename})
        return {'task_id': task.task_id, 'filename': filename}


@api.route('/<string:task_id>/status')
class Result(Resource):
    result_model = api.model('Result', {
        'status': fields.String,
        'result': fields.String
    })

    @api.response(200, 'Success', result_model)
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery_app)
        if task.ready():
            result = task.get()
        else:
            result = ''
        return {'status': task.status,
                'result': result}


@api.route('/image/<string:filename>')
class Image(Resource):
    def get(self, filename):
        mimetypes.init()
        with open(os.path.join(storage_folder, filename), 'rb') as file:
            return send_file(
                io.BytesIO(file.read()),
                mimetype=mimetypes.types_map[os.path.splitext(filename)[1]][1:]
            )


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)
