from db import session, db
from sqlalchemy import text
import pyexcel as p
from flask import make_response, jsonify


class ReportService:
    session_info = None

    def monthly(self, *args):
        print(args)
        sql = """
            select
             row_count() as SL_NO,
            DATE_FORMAT( sales0_.invoice_date, '%d/%m/%Y') as DATE,
             sales0_.invoice_number as INVOICE_NO,
             
            customers0_.business_name as AGENCY_NAME,
            customers0_.gst_reg_number as GST_NO,
            

             sales0_.total as TOTAL_AMOUNT,
             sales0_.total_before_tax as TAXABLE_AMOUNT,
            sales0_.cumilative_cgst as 'CGST%',
             sales0_.cumilative_igst as 'IGST%',
             sales0_.cumilative_sgst as 'SGST%'
                        from
             sales sales0_ ,customers customers0_
             where
             (
             MONTH(sales0_.invoice_date) = '{}'
             and YEAR(sales0_.invoice_date) = '{}'
             and sales0_.customer_id=customers0_.id
             ) 
            """.format(args[0]['month'], args[0]['year'])
        try:
            req_data = db.engine.execute(text(sql)).fetchall()
            return req_data
        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
            return res_json
