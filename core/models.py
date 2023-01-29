from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(BaseModel):
    name = models.CharField(max_length=40, unique=True, null=False, blank=False)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    validity_expiry_date = models.DateField(
        null=False, blank=False, default=datetime.now().date() + timedelta(days=365)
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.username} | {self.role.name}"

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
