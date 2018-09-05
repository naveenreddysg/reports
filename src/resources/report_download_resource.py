from flask import request, jsonify, json
from flask_restful import  Resource
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
import pyexcel as p
from flask import make_response, jsonify
from services.report_service import ReportService
from utils.util import model_to_dict

class ReportMonthlyResource (Resource):

    report_service = ReportService()

    @swag_from('../../spec/reports/monthly.yml')
    def get(self):
        try:
            req_data = self.report_service.monthly(request.args)
            if (len(req_data)) != 0:
                res_data = [[i[0] for i in req_data[0].items()]] + [list(i) for i in req_data]
                sheet = p.Sheet(res_data)
                output = make_response(sheet.csv)
                output.headers["Content-Disposition"] = "attachment; filename=export.csv"
                output.headers["Content-type"] = "text/csv"
                return output
            else:
                res_json = {'status': 1, 'message': 'No Data found in the specified range'}
                return jsonify(res_json)

        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
            return jsonify(res_json)