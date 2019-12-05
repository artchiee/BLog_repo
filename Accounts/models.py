# accounts.models.py
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from PIL import Image

# User manager
# Accounts.models.py


class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, password2=None, is_active=True):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        # if not full_name:
        #    raise ValueError('all users must have full name .. ')

        user = self.model(
            email=self.normalize_email(email),
            #full_name = full_name,
        )
        user.active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            # full_name,
            password=password,
        )
        user.staff_user = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            #full_name,
            password=password,
        )
        user.staff_user = True
        user.admin_user = True
        user.save(using=self._db)
        return user

    # MY new custom  user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active_user = models.BooleanField(default=True)
    #full_name = models.CharField(max_length=200, blank=True, null=True)
        # a admin user; non super-user
    staff_user = models.BooleanField(default=False)
    admin_user = models.BooleanField(default=False)  # a superuser

    # hook in the New Manager to our Model
    objects = UserManager()

    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['full_name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):      # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff_user

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin_user

    @property
    def is_active(self):
        "Is the user active?"
        return self.active_user 

    # Creating a model for User-Profile


class UserProfile(models.Model):

    # Give gender two choices
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    full_name = models.CharField(
        verbose_name='Full Name',  max_length=25, blank=True, null=True)
    user = models.OneToOneField(
        User, unique=True, related_name='profile_user', on_delete=models.CASCADE)
    address = models.CharField(
        max_length=200, verbose_name='Address', blank=True)
    phone_number = models.CharField(
        max_length=11, unique=True, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="media_deployment/Profile_images", default="media_deployment/Default_prof_img")
    gender = models.CharField(
        max_length=25,choices=gender_choice, verbose_name='Gender', default='Male')

    # Str methode to returne a name user profile
    def __str__(self):
        return f'{self.full_name}\'s Profile'

    def get_user_profile_name(self):
        return self.full_name
