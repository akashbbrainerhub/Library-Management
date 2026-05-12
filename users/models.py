from django.contrib.auth.models import AbstractUser
from django_mongodb_backend.fields import ObjectIdAutoField


class User(AbstractUser):
    id = ObjectIdAutoField(primary_key=True)
