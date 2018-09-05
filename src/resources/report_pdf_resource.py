from flask import request, jsonify, json, Response, make_response, request
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.report_print_service import ReportPrintService
import pdfkit

class ReportPdfResource (Resource):

    report_pdf_service = ReportPrintService()

    @swag_from('../../spec/reports/pdf.yml')
    def get(self):
        try:
            req_data = self.report_pdf_service.map_template(request.args)
            pdf = pdfkit.from_string(req_data, None)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = \
                'inline; filename=%s.pdf' % 'reports'
            return response

        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
            return jsonify(res_json)