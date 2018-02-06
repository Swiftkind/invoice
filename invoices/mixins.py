import os, errno

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template


from invoices.models import Invoice

from datetime import date 
from io import BytesIO
from io import StringIO
from PIL import Image
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa



class UserIsOwnerMixin(AccessMixin):
    """Check ownership request 
    """
    def dispatch(self, *args, **kwargs):
        """ Request ownership check
        """
        invoice = get_object_or_404(Invoice, id=kwargs['invoice_id'])
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user != invoice.owner:
            return redirect('index')
        return super().dispatch(self.request, *args, **kwargs)



class PdfMixin(object):
    """Generate a pdf
    """
    def render_to_pdf_and_view(self, template_src, context_dict={}):
        """Rendering a html file to pdf
        """
        template = get_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    def render_to_pdf_and_save(self, template_src, context_dict={}):
        """Rendering a html file to pdf
        """
        invoice_id = context_dict['invoice_id']
        template = get_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
        pdf_buff = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        pdf_directory = self.invoice_pdf_directory(invoice_id)
        fs = FileSystemStorage(pdf_directory)
        pdf_file = f"invoice_{invoice_id}.pdf"
        with fs.open(pdf_file, "wb") as pdf_save:
            pdf_save.write(pdf)
            return f"{pdf_directory}{pdf_file}"

    def invoice_pdf_directory(self,invoice_id):
        """ Get invoice pdf directory
        """
        directory = f"{settings.MEDIA_ROOT}invoices/{invoice_id}/"
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                return HttpResponse("Not found directory")
        return directory
