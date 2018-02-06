from django.db import models
from django.conf import settings


from phonenumber_field.modelfields import PhoneNumberField
from users.models import User, Company



class Client(models.Model):
    '''creating database model for client
    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client', default='')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    invoiced = models.BooleanField(default=False) 
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    mobile = PhoneNumberField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("display_name", "company"),("email","company"),("mobile","company"))

    def __str__(self):
        return f"{self.display_name}"