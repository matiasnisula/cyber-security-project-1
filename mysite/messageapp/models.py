from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Publication(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publisher")
    published = models.DateTimeField(auto_now_add=True)
    content = models.TextField()