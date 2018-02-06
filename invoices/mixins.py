from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings


from invoices.models import Invoice
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from io import BytesIO
from io import StringIO
from PIL import Image
from datetime import date 
import os, errno, io



class PdfMixin(object):
    """pdf functionality
    """
    def invoice_directory(self,_id, filename):
        """Directory to save pdf
        """
        directory = '{media}{invoices}/{id}/'.format(media=settings.MEDIA_ROOT,invoices='invoices',id=_id)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EXIST:
                    raise
        return '{media}{invoices}/{id}/{pdf}'.format(mdia=settings.MEDIA_ROOT,invoices='invoices',id=_id, pdf=filename)


    def get_invoice_directory(self,_id, filename):
        """Get directory pdf file
        """
        return 'invoices/{id}/{pdf}'.format(id=_id, pdf=filename)


    def save_pdf(self,  **kwargs):
        """saving invoice pdf
        """
        buff = BytesIO()
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        filename= str(self.invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
        image= str(settings.MEDIA_ROOT) + str(self.request.user.logo ) 
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format('invoice_' + str(invoice)+'.pdf')
        
        """Creating pdf layout
        """
        p = canvas.Canvas(filename)
        p.drawImage( image, 50,755, width=50, height=60) 
        p.drawString(50, 735, str(self.request.user.company))
        p.drawString(50, 715, str(self.request.user.country))
        p.drawString(50, 735, str(self.request.user.company))
        p.setFont('Times-Bold', 18)
        try:
            p.drawString(50,770, str(self.request.user.company_name) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,755, str(self.request.user.country) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,740, str(self.request.user.province) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,725, str(self.request.user.city) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,710, str(self.request.user.street) )
        except:
            p.drawString(10,10,'')
        p.setFont('Times-Bold', 30)
        p.drawString(450,770, 'INVOICE')
        p.setFont('Times-Bold', 18)
        p.drawString(450,755, '#: '+str(invoice.invoice_number) )
        p.drawString(450,715, 'Balance Due' )

        if invoice.invoice_type == 'fixed':
            p.drawString(450,695, str(invoice.amount) )
        if invoice.invoice_type == 'hourly':
            p.drawString(450,695, str(invoice.total_amount) )

        p.drawString(400, 675, 'Invoice date: '+str(invoice.invoice_date))
        p.drawString(400, 655, 'Due date: '+str(invoice.due_date))
        p.line(480,747,580,747)
        p.drawString(50,480, str(invoice.client.display_name) )
        p.drawString(50, 680, 'Type: '+str(invoice.invoice_date))
        p.drawString(50, 660, 'Type: '+str(invoice.due_date))
        p.drawString(50, 640, 'Type: '+str(invoice.order_number))
        p.drawString(50, 620, 'Type: '+str(invoice.invoice_type))
        p.drawString(50, 600, 'status: '+str(invoice.status))
        p.drawString(50, 580, 'paid: '+str(invoice.paid))
        p.drawString(50, 560, 'remarks: '+str(invoice.remarks))

        if invoice.rate:
            p.drawString(50, 520, 'rate: '+str(invoice.rate))
        if invoice.amount:
            p.drawString(50, 500, 'amount: '+str(invoice.amount))

        p.showPage()
        p.save()
        pdf = buff.getvalue()
        buff.close()
        response.write(pdf)
        return response


    def view_pdf(self,  **kwargs):
        """View pdf
        """
        response = HttpResponse(content_type='application/pdf')
        invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
        buff = BytesIO()

        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format('invoice_' + str(invoice)+'.pdf')
        
        """pdf layout
        """
        p = canvas.Canvas(buff)
        p.setFont('Times-Bold', 18)
        try:
            p.drawString(50,770, str(self.request.user.company_name) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,755, str(self.request.user.country) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,740, str(self.request.user.province) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,725, str(self.request.user.city) )
            p.setFont('Times-Bold', 18)
            p.drawString(50,710, str(self.request.user.street) )
        except:
            p.drawString(10,10,'')
        p.setFont('Times-Bold', 30)
        p.drawString(450,770, 'INVOICE')
        p.setFont('Times-Bold', 18)
        p.drawString(450,755, '#: '+str(invoice.invoice_number) )
        p.drawString(50,480, str(invoice.client.display_name) )
        p.drawString(50, 680, 'Type: '+str(invoice.invoice_date))
        p.drawString(50, 660, 'Type: '+str(invoice.due_date))
        p.drawString(50, 640, 'Type: '+str(invoice.order_number))
        p.drawString(50, 620, 'Type: '+str(invoice.invoice_type))
        p.drawString(50, 600, 'status: '+str(invoice.status))
        p.drawString(50, 580, 'paid: '+str(invoice.paid))
        p.drawString(50, 560, 'remarks: '+str(invoice.remarks))
        if invoice.rate:
            p.drawString(50, 520, 'rate: '+str(invoice.rate))
        if invoice.amount:
            p.drawString(50, 500, 'amount: '+str(invoice.amount))
        p.showPage()
        p.save()
        pdf = buff.getvalue()
        buff.close()
        response.write(pdf)
        return HttpResponse(response,content_type='application/pdf')

