from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(BaseModel):
    name = models.CharField(max_length=40, unique=True, null=False)
    is_active = models.BooleanField(null=False, default=True)


class User(AbstractUser, BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
