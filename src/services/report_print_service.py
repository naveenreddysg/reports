from pybars import Compiler
import os
from db import session, db
from sqlalchemy import text
from num2words import num2words

class ReportPrintService:
    session_info = None

    def get_data(self, id):
        print(id)
        sql = """
                select 
                sl.id as id,
                sl.invoice_number as invoiceNumber,
                DATE_FORMAT(sl.invoice_date, '%d-%m-%Y') as invoiceDate,
                format(sl.total_before_tax, 2, 'en_IN') as subtotal  ,
                format(sl.cumilative_cgst, 2, 'en_IN') as cgst  ,
                format(sl.cumilative_sgst, 2, 'en_IN') as sgst  ,
                format(sl.cumilative_igst, 2, 'en_IN') as igst  ,
                format( sl.cumilative_cgst + sl.cumilative_sgst, 2, 'en_IN') as gst,
                format(sl.discount_value, 2, 'en_IN') as discount ,
                format(sl.cessValue, 2, 'en_IN') as cess,
                format(sl.cumilative_tax, 2, 'en_IN') as tax  ,
                format(sl.total, 2, 'en_IN') as total  ,
                sl.invoice_message as invoiceMessage  ,
                concat(cu.first_name, ' ' , cu.last_name) as customerName, 
                cu.mobile as customerMobile,
                cu.email as customerEmail,
                cua.lane as customerLane,
                cua.street as customerSteet,
                cua.city as customerCity,
                cua.area as customerArea,
                cua.state as customerState,
                cua.country as customerCountry,
                cua.zipcode as customerZipcode,
                cp.name as companyName,
                cp.tan as compnayTan,
                cp.company_code as compnayCode,
                cp.website as companyWebsite,
                cpa.lane as companyLane,
                cpa.street as companySteet,
                cpa.city as companyCity,
                cpa.area as companyArea,
                cpa.state as companyState,
                cpa.country as companyCountry,
                cpa.zipcode as companyZipcode,
                cb.bank_name as bankName,
                cb.bank_account_number as accountNumber,
                cb.ifsc_code as ifscCode
                from sales as sl
                inner join customers as cu on ( cu.id = sl.customer_id)
                inner join company as cp on ( cp.id = sl.company_id)
                inner join address as cua on (cua.id = cu.address_id)
                inner join address as cpa on (cpa.id = cu.address_id)
                left join company_bank_details as cb on (cb.company_id = cu.company_id)
                where sl.id = "{}";
            """.format(id)

        sql2 = """
                select 
                    pd.product_name as productName,
                    pd.hsn_code as productHsnCode,
                    format(si.quantity_purchased, 2) as Qty,
                    format(si.item_unit_price, 2, 'en_IN') as Rate,
                    format(si.total_amount, 2, 'en_IN') as Amount,
                    format(si.cgs_gst + si.sgs_gst, 2, 'en_IN') as gst,
                    format(si.tax_amount, 2, 'en_IN') as gstAmount,
                    format(si.total_after_tax, 2, 'en_IN') as TotalAfterTax
                    from sales_items as si
                    inner join inv_products as pd on (pd.id = si.product_id)
                    where si.sale_id = '{}';
                """.format(id)

        sql3 = """
               select 
                   sv.service_name as serviceName,
                   sv.service_code as serviceCode,
                   format(si.quantity_purchased, 2) as Qty,
                   format(si.item_unit_price, 2, 'en_IN') as Rate,
                   format(si.total_amount, 2, 'en_IN') as Amount,
                   format(si.cgs_gst + si.sgs_gst, 2, 'en_IN') as gst,
                   format(si.tax_amount, 2, 'en_IN') as gstAmount,
                   format(si.total_after_tax, 2, 'en_IN') as TotalAfterTax
                   from sales_items as si
                   inner join inv_services as sv on (sv.id = si.service_id)
                   where si.sale_id = '{}';
               """.format(id)
        try:
            req_data = db.engine.execute(text(sql)).fetchall()
            res_data = dict(req_data[0].items())
            req_data2 = db.engine.execute(text(sql2)).fetchall()
            res_data2 = [dict(i.items()) for i in req_data2]
            # print(res_data2)
            req_data3 = db.engine.execute(text(sql3)).fetchall()
            res_data3 = [dict(i.items()) for i in req_data3]
            # print(res_data3)
            total_value = float(res_data['total'].replace(',', ''))
            total_value = (num2words(round(total_value), lang='en_IN'))
            res_data['ItoW'] = (total_value.title().replace(',', ''))
            if len(res_data2) != 0:
                for i in res_data2:
                    i['SNo'] = res_data2.index(i) + 1
                res_data['products'] = res_data2
            if len(res_data3) != 0:
                for i in res_data3:
                    i['SNo'] = res_data3.index(i) + 1
                res_data['services'] = res_data3
            return res_data

        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
            return res_json

    def map_template(self, *args):
        source = self.get_data(args[0]['id'])
        # print(source)
        abs_file_path = os.path.join(os.path.dirname(__file__),
                                     '../../templates/report.html')
        with open(abs_file_path) as data_file:
            data = data_file.read()
        compiler = Compiler()
        template = compiler.compile(data)
        output = template(source)
        return output