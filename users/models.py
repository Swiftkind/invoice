from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from users.utils import get_user_directory, get_company_directory
import os



class UserManager(BaseUserManager):

    def _create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError('The given Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):


        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        kwargs.setdefault('is_active', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **kwargs)



class Company(models.Model):

	company_name = models.CharField(max_length=255, default='')
	logo = models.ImageField(upload_to=get_company_directory,null=True, blank=True, default='') 
	country = models.CharField(max_length=200, default="Philippines")
	province = models.CharField(max_length=200, default='', null=True, blank=True)
	city = models.CharField(max_length=200, default='', null=True, blank=True)
	street = models.CharField(max_length=200, default='', null=True, blank=True)

	owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, related_name = 'owner_company',default='', null=True)
	#member = models.ForeignKey(User, on_delete=models.SET_NULL, related_name = 'user_company',default='', null=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.company_name)



class User(PermissionsMixin,AbstractBaseUser):
	
	name = models.CharField(max_length=255, default='')
	email = models.EmailField(max_length=255, unique=True, default='')
	avatar = models.ImageField(upload_to=get_user_directory,null=True, blank=True, default='')

	company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(_('activate'), default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	#REQUIRED_FIELDS = ['email']

	_avatar = None


	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self._avatar = self.avatar

	def __str__(self):
		return '{}'.format(self.name)

	def save(self, *args, **kwargs):
		if self.avatar != self._avatar and self._avatar != '':
			self.delete_avatar()
		return super(User, self).save(*args, **kwargs)
		self._avatar = self.avatar

	def delete_avatar(self, empty_image=False):
		image_path = os.path.join(settings.MEDIA_ROOT, str(self._avatar))

		try:
			os.remove(image_path)
		except Exception as e:
			pass

		if empty_image:
			self.avatar = ''

	def clean(self):
		super(User, self).clean()
		self.email = self.__class__.objects.normalize_email(self.email)



