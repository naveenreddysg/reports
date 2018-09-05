# amount = "12,123.00"
# print(float());amount.replace(',', '')
import pdfkit
pdfkit.from_url('http://localhost:2002/reports/print', 'out.pdf')


