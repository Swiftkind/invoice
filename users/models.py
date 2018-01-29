from django.db.models import OneToOneField,Model,ForeignKey, CASCADE,SET_NULL, EmailField,CharField,DateTimeField, BooleanField, ImageField
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



class User(PermissionsMixin,AbstractBaseUser):
	
	name = CharField(max_length=255, default='')
	email = EmailField(max_length=255, unique=True, default='')
	company =  CharField(max_length=255, default='')
	logo = ImageField(upload_to=get_company_directory,null=True, blank=True, default='') 
	avatar = ImageField(upload_to=get_user_directory,null=True, blank=True, default='')
	country = CharField(max_length=200, default="Philippines")
	province = CharField(max_length=200, default='')
	city = CharField(max_length=200, default='')
	street = CharField(max_length=200, default='')

	date_created = DateTimeField(auto_now_add=True)
	date_updated = DateTimeField(auto_now=True)

	is_superuser = BooleanField(default=False)
	is_staff = BooleanField(default=False)
	is_active = BooleanField(_('activate'), default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	#REQUIRED_FIELDS = ['email']

	_avatar = None
	_logo = None

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		unique_together = (("name", "company"),)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self._avatar = self.avatar
		self._logo = self.logo

	def __str__(self):
		return self.name
		#return "{email}".format(email=self.email)

	def save(self, *args, **kwargs):
		if self.avatar != self._avatar and self._avatar != '':
			self.delete_avatar()
		if self.logo != self._logo and self._logo != '':
			self.delete_logo()

		return super(User, self).save(*args, **kwargs)
		self._avatar = self.avatar
		self._logo = self.logo

	def delete_avatar(self, empty_image=False):
		image_path = os.path.join(settings.MEDIA_ROOT, str(self._avatar))

		try:
			os.remove(image_path)
		except Exception as e:
			pass

		if empty_image:
			self.avatar = ''

	def delete_logo(self, empty_image=False):
		image_path = os.path.join(settings.MEDIA_ROOT, str(self._logo))

		try:
			os.remove(image_path)
		except Exception as e:
			pass

		if empty_image:
			self.logo = ''


	def clean(self):
		super(User, self).clean()
		self.email = self.__class__.objects.normalize_email(self.email)


#class SubUser(User):
#	user_ptr = settings.AUTH_USER_MODEL
#	owner = OneToOneField(settings.AUTH_USER_MODEL,on_delete=CASCADE, related_name='sub_user',parent_link=True,default='')
#	email1 = EmailField(max_length=255, unique=True, default='')
	#parent_user = CharField(max_length=255)
#	email = EmailField(max_length=255)
#	password = CharField(max_length=50)



#	def __str__(self):
#		return '{}'.format(self.email)
	'''
	def save(self, *args, **kwargs):
		import pdb; pdb.set_trace()
		self.parent_user = request.user
		super(Subuser, self).save(*args, **kwargs)
	'''

'''
	parent_user = 
	email
	password
'''