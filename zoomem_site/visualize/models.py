from django.db import models

# Create your models here.

class CodeData(models.Model):
    code = models.TextField()
    code_input = models.TextField(blank=True)
    code_key = models.TextField()
