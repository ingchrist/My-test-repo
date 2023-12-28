from typing import TypeVar
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from utils.base.email_service import email_service
from utils.base.logger import err_logger, logger  # noqa
from utils.base.validators import validate_special_char, validate_phone
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.base.general import get_random_string


T = TypeVar('T', bound=AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_base_user(
        self, email, is_active=True,
        is_staff=False, is_admin=False
    ) -> T:
        if not email:
            raise ValueError("User must provide an email")

        user: User = self.model(
            email=self.normalize_email(email)
        )
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(
        self, email, password=None, is_active=True,
        is_staff=False, is_admin=False
    ) -> T:
        user = self.create_base_user(email, is_active, is_staff, is_admin)
        if not password:
            raise ValueError("User must provide a password")
        user.set_password(password)
        user.save()
        return user

    def create_staff(self, email, password=None) -> T:
        user = self.create_user(email=email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None) -> T:
        user = self.create_user(
            email=email, password=password, is_staff=True, is_admin=True)
        return user

    def get_staffs(self):
        return self.filter(staff=True)

    def get_admins(self):
        return self.filter(admin=True)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    # Admin fields
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    verified_email = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def username(self) -> str:
        return self.profile.username

    @property
    def get_emailname(self) -> str:
        """Return the A part of an email e.g [A]@[TLD].com"""
        return self.email.split('@')[0]

    def __str__(self) -> str:
        return self.email

    def email_user(self, subject, message):
        """
        Send an email to this user.

        :param subject: subject of the email
        :type subject: str
        :param message: message to be sent
        :type message: str
        :return: True if email was sent successfully, False otherwise
        :rtype: bool
        """
        return email_service.send_message(
            subject=subject, message=message, email=self.email)

    @property
    def first_name(self) -> str:
        return self.profile.first_name

    @property
    def last_name(self) -> str:
        return self.profile.last_name

    @property
    def is_active(self) -> bool:
        return self.active

    @property
    def is_staff(self) -> bool:
        return self.staff

    @property
    def is_admin(self) -> bool:
        return self.admin


class Profile(models.Model):
    ACCOUNT_TYPES = [
        ('logistics', 'Logistics',),
        ('transportation', 'Transportation',),
        ('driver', 'Driver',),
    ]

    account_type = models.CharField(
        choices=ACCOUNT_TYPES, max_length=30, blank=True)
    approved = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=60, unique=True, validators=[validate_special_char])
    created = models.DateTimeField(auto_now=True)

    first_name = models.CharField(
        max_length=30, validators=[validate_special_char])
    last_name = models.CharField(
        max_length=30, validators=[validate_special_char])

    phone = models.CharField(max_length=20, validators=[validate_phone])
    image = models.ImageField(
        upload_to='accounts/profiles', null=True, blank=True)

    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=60, blank=True)
    zip = models.CharField(max_length=6, blank=True)

    about = models.TextField(max_length=2500, blank=True)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.get_fullname

    @property
    def get_fullname(self) -> str:
        return self.fullname.title()

    def get_user_name_with_id(self) -> str:
        user_name = self.first_name + self.last_name
        return '-'.join([user_name, str(self.user.id)])


class NewsletterSubscriber(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    """This is used to store reason for users
    unsubscribing from the website email newsletter"""
    reason = models.TextField(blank=True)

    def __str__(self):
        return self.email


class UsedResetToken(models.Model):
    """
    Model for used tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.profile.fullname


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created, **kwargs):
    if created:
        try:
            Profile.objects.get(username=instance.get_emailname)
            unique_username = f"{instance.get_emailname}{get_random_string(4)}"
            Profile.objects.create(user=instance, username=unique_username)
        except Profile.DoesNotExist:
            Profile.objects.create(
                user=instance, username=instance.get_emailname)
