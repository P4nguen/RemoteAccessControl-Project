from django.db import models

# Create your models here.

class Agent(models.Model):
    port = models.IntegerField()
    user = models.CharField(max_length=100)
    #target_ip = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.user