from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin

from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from invoices.models import Invoice

from io import BytesIO
from io import StringIO

from PIL import Image

from datetime import datetime, date 
import os, errno,io



class PdfMixin(object):

	def invoice_directory(self,_id, filename):
		directory = '{media}{invoices}/{id}/'.format(media=settings.MEDIA_ROOT,invoices='invoices',id=_id)
		if not os.path.exists(directory):
			try:
				os.makedirs(directory)
			except OSError as e:
				if e.errno != errno.EEXIST:
 					raise
		return '{media}{invoices}/{id}/{pdf}'.format(media=settings.MEDIA_ROOT,invoices='invoices',id=_id, pdf=filename)

	def get_invoice_directory(self,_id, filename):
		return 'invoices/{id}/{pdf}'.format(id=_id, pdf=filename)

	def save_pdf(self,  **kwargs):
		#import pdb; pdb.set_trace()
		response = HttpResponse(content_type='application/pdf')
		#response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		#filename = '{media}{files}/{id}/{invoice}'.format(media=settings.MEDIA_ROOT, files='invoices', id=invoice.id, invoice='invoice_' + str(invoice))
		#filename = settings.MEDIA_ROOT+'invoices/'+str(invoice.id)+'/invoice_' + str(invoice)
		#'invoices/{id}/{pdf}'.format(id=self.id, pdf=filename)
		
		#filename='{0}.pdf'.format(filename)
	
		filename=str(self.invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
		response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format('invoice_' + str(invoice)+'.pdf')
		buff = BytesIO()
		#tmp = StringIO()
		p = canvas.Canvas(filename)
		
		image= str(settings.MEDIA_ROOT) + str(self.request.user.logo ) 
		p.drawImage( image, 50,755, width=50, height=60) 
		#image.hAlign = 'CENTER'
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
		#import pdb; pdb.set_trace()
		response = HttpResponse(content_type='application/pdf')
		invoice = get_object_or_404(Invoice, pk=kwargs['invoice_id'])
		#filename=str(self.invoice_directory(_id=invoice.client.id,filename='invoice_' + str(invoice)+'.pdf') )
		response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format('invoice_' + str(invoice)+'.pdf')
		buff = BytesIO()
		#tmp = StringIO()
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


		