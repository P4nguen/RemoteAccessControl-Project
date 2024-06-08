from django.db import models

# Create your models here.
class Report(models.Model):
    agent = models.ForeignKey('agents.Agent', on_delete=models.CASCADE, default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    result = models.TextField()
    attack = models.TextField()

    def __str__(self):
        return self.user