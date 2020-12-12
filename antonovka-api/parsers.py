from flask_restplus import reqparse
import werkzeug

file_upload = reqparse.RequestParser()
file_upload.add_argument('file',
                         type=werkzeug.datastructures.FileStorage,
                         required=True,
                         location='files')
