import os
from celery.result import AsyncResult
from flask import Flask, Blueprint, Response, flash, request, redirect, send_file, abort
from flask_restplus import Api, Resource, fields
from tasks import predict
from tasks import app as celery_app

app = Flask(__name__, static_url_path='/static')
api = Api(version='1.0')

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
app.register_blueprint(blueprint)


@api.route('/predict')
class Predict(Resource):
    task_model = api.model('Task', {
        'task_id': fields.String
    })

    @api.response(200, 'Task enqueued successfully', task_model)
    def get(self):
        print("start")
        task = predict.apply_async(routing_key='predict')
        return {'task_id': task.task_id}


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


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)
