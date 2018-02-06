import os

from django.conf import settings
from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from users.utils import get_user_directory, get_company_directory



class UserManager(BaseUserManager):
    """Manage user
    """
    def _create_user(self, email, password, **kwargs):
        """Create user
        """
        if not email:
            raise ValueError('The given Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        """Set default for user
        """
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_active', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """Set default for superuser
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **kwargs)



class Company(models.Model):
    """Creating company model database
    """
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=200, default="Philippines")
    city = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to=get_company_directory, null=True, blank=True) 
    province = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    _logo = None

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)
        self._logo = self.logo

    def save(self, *args, **kwargs):
        """Save user dealing with avatar
        """
        if self.logo != self._logo and self._logo != '':
            self.delete_avatar()
        return super(Company, self).save(*args, **kwargs)
        self._logo = self.logo

    def delete_avatar(self, empty_image=False):
        """Delete function avatar
        """
        image_path = os.path.join(settings.MEDIA_ROOT, str(self._logo))
        try:
            os.remove(image_path)
        except Exception as e:
            pass
        if empty_image:
            self.logo = ''

    def __str__(self):
        """Strin representation of model company
        """
        return f"{self.name}"



class User(AbstractBaseUser, PermissionsMixin):
    """Create user model database
    """
    avatar = models.ImageField(upload_to=get_user_directory,null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True
        )
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('activate'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    _avatar = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._avatar = self.avatar

    def __str__(self):
        """String representation of the user model
        """
        return f"{self.email}"

    def save(self, *args, **kwargs):
        """Save user dealing with avatar
        """
        if self.avatar != self._avatar and self._avatar != '':
            self.delete_avatar()
        return super(User, self).save(*args, **kwargs)
        self._avatar = self.avatar

    def delete_avatar(self, empty_image=False):
        """Delete function avatar
        """
        image_path = os.path.join(settings.MEDIA_ROOT, str(self._avatar))
        try:
            os.remove(image_path)
        except Exception as e:
            pass
        if empty_image:
            self.avatar = ''


    def get_full_name(self):
        """Return the full name of the user
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_short_name(self):
        """Return shortname of user
        """
        return f"{self.first_name} {self.last_name}"

    def get_avatar_url(self):
        """Get the url of avatar
        """
        return reverse('profile', args=[self.id])

    def clean(self):
        """Clean email
        """
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)



