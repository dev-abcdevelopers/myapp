from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        db_table = 'admin_users'
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",
        related_query_name="customuser",
    )

class UserAPIKey(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='api_key')
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s API Key"
    

class PublicUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

class APIAccessLog(models.Model):
    api_key = models.ForeignKey(UserAPIKey, on_delete=models.CASCADE, null=True, blank=True)
    accessed_at = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
    success = models.BooleanField(default=True)

    def __str__(self):
        return f"Access by {self.api_key.user.username} on {self.accessed_at}"
