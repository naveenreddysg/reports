from flask import Flask, request
from flask_jwt import JWT
from flask_restful import Api
from config import app_config
from flasgger import Swagger
import os
import datetime

config_name = os.getenv('WEB_ENV', 'dev')
print("WEB_ENV=", config_name)
app = Flask(__name__, instance_relative_config=False)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response


app.config.from_object(app_config[config_name])
#app.config.from_pyfile('config.py')

# from utils.security_user import SecurityUser
#
# JWT.JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=9999999)
# app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=9999999)
# jwt = JWT(app, SecurityUser.authenticate, SecurityUser.identity)
#
# api.add_resource(SecurityUser, '/auth')


from resources.report_download_resource import ReportMonthlyResource
api.add_resource(ReportMonthlyResource, '/reports/download/monthly')

from resources.report_print_resource import ReportPrintResource
api.add_resource(ReportPrintResource, '/reports/print')

from resources.report_pdf_resource import ReportPdfResource
api.add_resource(ReportPdfResource, '/reports/pdf')

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', "Authorization, Content-Type")
#     response.headers.add('Access-Control-Expose-Headers', "Authorization")
#     response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
#     response.headers.add('Access-Control-Allow-Credentials', "true")
#     response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
#     return response

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response
    # if request.method == 'OPTIONS':
    #     response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
    #     headers = request.headers.get('Access-Control-Request-Headers')
    #     if headers:
    #         response.headers['Access-Control-Allow-Headers'] = headers
    # header = request.headers.get('Authorization')
    # if header:
    #     _, token = header.split()
    #     request.identity = SecurityUser.identity(jwt.jwt_decode_callback(token))
    #     print(request.identity)
    # return response

if __name__ == '__main__':
    app.config['SWAGGER'] = {
        "swagger_version": "2.0",
        "title": "ABCD",
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
    }
    # Swagger(app, template={
    #     "swagger": "3.0",
    #     "consumes": [
    #         "application/json",
    #         "application/x-www-form-urlencoded",
    #     ],
    #     "produces": [
    #         "application/json",
    #     ],
    #     "securityDefinitions": {
    #         "jwt": {
    #             "type": 'apiKey',
    #             "name": 'Authorization',
    #             "in": 'header'
    #         }
    #     },
    #     "security": [
    #         {"jwt": []}
    #     ]
    # },)
    swagger_config = {
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: False,
            }
        ],
        'swagger_ui': False,
    }
    Swagger(app, config=swagger_config, template={
        "swagger": "3.0",
        "headers": [
        ],
        "consumes": [
            "application/json",
            "application/x-www-form-urlencoded",
        ],
        "produces": [
            "application/json",
        ],
        "securityDefinitions": {
            "jwt": {
                "type": 'apiKey',
                "name": 'Authorization',
                "in": 'header'
            }
        },
        "security": [
            {"jwt": []}
        ]

    })

    from db import db
    db.init_app(app)
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])