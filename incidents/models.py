from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    type = models.CharField(max_length=100)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    incident_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.type
