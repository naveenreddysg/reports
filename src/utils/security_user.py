from flasgger import swag_from
from flask_restful import  Resource
from flask import request, jsonify, json
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from db import db
from sqlalchemy import text
from utils.util import random_number

class JwtIdentify(object):
    def __init__(self, id):
        self.id = id


class SecurityUser(Resource):

    @swag_from('../../spec/app/auth.yml', methods=['POST'])
    def post(self):
        print("inside post")
        pass

    @staticmethod
    def authenticate(username, password):
        param = {}
        param["vid"] = username.split('-')[0]
        param["userid"] = username.split('-')[1]
        param["password"] = password
        print(param)
        sql = """
            select
                id,
                name,
                email,
                mobile,
                role,
                branch_id,
                vid
            from profile 
            where vid = '{vid}'
            and (email = '{userid}' or mobile = '{userid}')
            and password = '{password}'
        """.format(**param)
        print(sql)
        print("inside authenticate")
        result = db.engine.execute(text(sql)).first();
        print(result)
        if result and result[0]:
            user = {}
            user['id'] = result[0]
            user['name'] = result[1]
            user['email'] = result[2]
            user['mobile'] = result[3]
            user['role'] = result[4]
            user['branchId'] = result[5]
            user['vid'] = result[6]
            # user['id'] = 'SUPPORT_DFF_USER'
            # user['name'] = 'Support User'
            # user['email'] = 'support@dfftech.com'
            # user['mobile'] = '123456789'
            # user['role'] = 'SuperAdmin'
            # user['vid'] = 'DFF'
            print(user)
            return JwtIdentify(user)
        else:
            return None

    @staticmethod
    def identity(payload):
        jwt_identity = payload['identity']
        return jwt_identity

    @swag_from('../../spec/app/forgot_password.yml')
    def get(self):
        res_json = {}
        data = {}
        param = {}
        param["vid"] = request.args['vid']
        param["userid"] = request.args['userid']

        if param["vid"] and param["userid"]:
            sql = """
                select
                    id
                from profile 
                where vid = '{vid}'
                and (email = '{userid}' or mobile = '{userid}')
            """.format(**param)
            result = db.engine.execute(text(sql)).first();
            if result and result[0]:
                param["token"] = random_number(4)
                sql = """
                    update profile set
                        token = '{token}'
                    where vid = '{vid}'
                    and (email = '{userid}' or mobile = '{userid}')
                """.format(**param)
                db.engine.execute(text(sql));
                res_json['status'] = 1
                data['message'] = "your token: {}".format(param["token"])
            else:
                res_json['status'] = 0
                data['message'] = "Invalid email or mobile."
        else:
            res_json['status'] = 0
            data['message'] = "Please provide vendor id and email or mobile."

        res_json['data'] = data
        return jsonify(res_json)

    @swag_from('../../spec/app/reset_password.yml')
    def put(self):
        res_json = {}
        data = {}
        param = {}
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)

        param["vid"] = req_data.get('vid', None)
        param["userid"] = req_data.get('userid', None)
        param["password"] = req_data.get('password', None)
        param["token"] = req_data.get('token', None)



        if param["vid"] and param["userid"] and param["password"] and param["token"]:
            sql = """
                select
                    id
                from profile 
                where vid = '{vid}'
                and (email = '{userid}' or mobile = '{userid}')
                and token = '{token}'
            """.format(**param)
            result = db.engine.execute(text(sql)).first();
            if result and result[0]:
                param["token"] = random_number(4)
                sql = """
                    update profile set
                        token = null
                        and password = '{password}'
                    where vid = '{vid}'
                    and (email = '{userid}' or mobile = '{userid}')
                """.format(**param)
                db.engine.execute(text(sql));
                res_json['status'] = 1
                data['message'] = "your password updated successfully."
            else:
                res_json['status'] = 0
                data['message'] = "Invalid token or email or mobile."
        else:
            res_json['status'] = 0
            data['message'] = "Please provide required details."

        res_json['data'] = data
        return jsonify(res_json)