import os


from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404

from users.models import User, Company




register = template.Library()

# asks for a user object and returns appropriate img.
@register.simple_tag
def get_profile_pic(user_id):
    """ Get the image
    """
    user = get_object_or_404(User, id=user_id)
    if user.avatar:
        return f"{user.avatar.url}"
    return settings.DEFAULT_IMAGE



@register.simple_tag
def get_company_logo_pic(user_id):
    """ Get the image
    """
    try:
        company = get_object_or_404(Company, owner=user_id)
        if company.logo:
            return f"{company.logo.url}"
    except:
        return settings.DEFAULT_IMAGE