from flask import request, jsonify, json, Response, make_response, request
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.report_print_service import ReportPrintService
from utils.util import model_to_dict

class ReportPrintResource (Resource):

    report_print_service = ReportPrintService()

    @swag_from('../../spec/reports/print.yml')
    def get(self):
        try:
            req_data = self.report_print_service.map_template(request.args)
            print(req_data)
            response = make_response(req_data)
            response.headers['content-type'] = 'application/octet-stream'
            return response

        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
            return jsonify(res_json)