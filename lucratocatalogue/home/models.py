from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class CatalogueUserManager(BaseUserManager):
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name='admin',
            last_name='zhang',
            is_seller=True,
            is_editor=True,
            company='Saxion'
        )
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, is_seller, is_editor, company):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_seller=is_seller,
            is_editor=is_editor,
            company=company
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_editor(self, email, password, f_name, l_name, c_name):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=f_name,
            last_name=l_name,
            is_seller=False,
            is_editor=True,
            company=c_name
        )
        user.is_admin = True
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_seller(self, email, password, f_name, l_name, c_name):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=f_name,
            last_name=l_name,
            is_seller=True,
            is_editor=False,
            company=c_name
        )
        user.is_admin = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user


class Label(models.Model):
    type = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.description

    @property
    def type(self):
        return self.type


class Item(models.Model):
    title = models.CharField(max_length=20)
    cover_picture = models.ImageField()
    detail_picture_1 = models.ImageField()
    detail_picture_2 = models.ImageField()
    video_address = models.TextField()
    qr_code = models.ImageField()
    description = models.TextField()
    seller_info = models.TextField()
    labels = models.ManyToManyField('home.Label', related_name='item_labels')

    def __str__(self):
        return self.title


class CatalogueUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_seller = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    company = models.TextField()
    favorites = models.ManyToManyField('home.Item', related_name='favorite_items')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CatalogueUserManager()

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

    @property
    def name(self):
        return str(self.first_name) + " " + str(self.last_name)

    @property
    def isSeller(self):
        return self.is_seller

    @property
    def isEditor(self):
        return self.is_editor

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def favorites(self):
        return self.favorites
