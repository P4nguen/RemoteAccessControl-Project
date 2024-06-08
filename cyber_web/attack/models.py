from django.db import models

# Create your models here.
class Attack(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip