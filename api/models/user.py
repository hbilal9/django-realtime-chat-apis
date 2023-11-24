from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .profile import Profile

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SUPERADMIN = 'superadmin', 'SuperAdmin'
        USER = 'user', 'User'
        COMPANY = 'company', 'Company'
        ENGINEER = 'engineer', 'engineer'
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    ACCOUNT_TYPES = [
        ('user', 'user'),
        ('engineer', 'engineer'),
        ('business', 'business'),
    ]

    base_role = Role.USER
    createsuperuser_role = Role.SUPERADMIN

    role = models.CharField(max_length=20, choices=Role.choices, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    remember_token = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.createsuperuser_role if self.is_superuser else self.base_role
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cover = self.cover
        avatar = self.avatar
        if cover:
            cover.delete()
        if avatar:
            avatar.delete()
        super().delete(*args, **kwargs)

    def fullName(self):
        return f"{self.first_name} {self.last_name}"

    # add a related_name argument to avoid conflicts with default User model
    # groups = models.ManyToManyField(Group, related_name='user_set', blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='user_set', blank=True)


# class AdminUser(User):
#     base_role = User.Role.ADMIN
#     class Meta:
#         proxy = True



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and (instance.account_type == 'individual' or instance.account_type == 'employee'):
#         Profile.objects.create(user=instance)
#     elif created and instance.account_type == 'business':
#         company_name = instance.company_name
#         Company.objects.create(user=instance, name=company_name)