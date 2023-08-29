from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('faculty', 'Faculty'),
        ('service_provider', 'Service Provider'),
        ('student', 'Student'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_name_display()} - {self.code}"