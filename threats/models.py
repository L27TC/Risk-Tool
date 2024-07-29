from django.db import models
from django.conf import settings  # Add this import

class Threat(models.Model):
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Update this line
        on_delete=models.CASCADE
    )
    # Other fields...

