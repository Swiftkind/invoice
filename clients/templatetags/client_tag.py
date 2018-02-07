import os

from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404


from clients.models import Client


register = template.Library()

# asks for a user object and returns appropriate img.
@register.simple_tag
def get_client_company_logo(client_id):
    """ Get the image
    """
    try:
        client = get_object_or_404(Client, id=client_id)
        if client.client_company_logo != None or client.client_company_logo != '':
            return f"{client.client_company_logo.url}"
    except:
        return settings.DEFAULT_IMAGE