from django.db import models
from django.conf import settings


from clients.utils import get_client_company_logo_dir
from phonenumber_field.modelfields import PhoneNumberField
from users.models import User, Company


class Client(models.Model):
    """ Create database model for client
    """
    client_company = models.CharField(max_length=100)
    client_company_logo = models.ImageField(upload_to=get_client_company_logo_dir, 
                                            null=True, 
                                            blank=True
                          )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    invoiced = models.BooleanField(default=False)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.CASCADE, 
                              related_name='client', 
                              default=''
            )

    class Meta:
        unique_together = (("client_company", "company"),("email","company"),("mobile","company"))

    def __str__(self):
        return f"{self.client_company}"