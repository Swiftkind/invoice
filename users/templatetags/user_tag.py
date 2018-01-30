from django import template
from users.models import User, Company
from django.conf import settings
import os

register = template.Library()

# asks for a user object and returns appropriate img.
@register.simple_tag
def get_profile_pic(user_id):

    # get the image
    user = User.objects.get(id=user_id)
    if user.avatar:
        return '{}'.format(user.avatar.url)
    return '/static/img/default.png'

@register.simple_tag
def get_company_logo_pic(user_id):

    # get the image
    company = Company.objects.get(owner=user_id)
    if company.logo:
        return '{}'.format(company.logo.url)
    return '/static/img/default.png'