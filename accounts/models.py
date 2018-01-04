from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .utils import get_directory
import os

# Create your models here.
class AccountManager(BaseUserManager):
    """
    Manager class which contains methods used by the account model
    """
    #use_in_migrations = True
    def _create_user(self, email, password, **kwargs):
        """ save user account using email and password
        """
        if not email:
            raise ValueError('The given Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        """ sets the defaults for user account
        """
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """ sets the defaults for superuser account
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **kwargs)



class Account(AbstractBaseUser, PermissionsMixin):
    """
    Model class that contains account information
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = models.EmailField(verbose_name='email address',max_length=255, unique=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    avatar = models.ImageField(upload_to=get_directory, null=True, blank=True)
    nick_name = models.CharField(max_length=40, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    timezone = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=225, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)

    

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email']

    _avatar = None

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self._avatar = self.avatar

    def __str__(self):
        return "{email}".format(email=self.email)

    def save(self, *args, **kwargs):
        #if not self.timezone:
        #    self.timezone = self.get_gmt()

        if self.avatar != self._avatar and self._avatar != '':
            self.delete_avatar()

        return super(Account, self).save(*args, **kwargs)
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
        super(Account, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    #def get_gmt(self):
    #    return "GMT {}".format(self.get_gmtzone(self.city))

    #@property
    #def is_staff(self):
    #    return self.is_admin
