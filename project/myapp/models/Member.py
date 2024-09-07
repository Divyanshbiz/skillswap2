from django.db import models

class Member(models.Model):
    username=models.CharField(max_length=100, unique=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    skills = models.TextField(blank=True)  # Store skills as a comma-separated string
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    