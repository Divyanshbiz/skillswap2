from django.db import models
from myapp.models.Member import Member  # Import Member model correctly
from django.utils import timezone  # Import timezone utility

class VideoConference(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True, default='thumbnails/default-thumbnail.png')
    host = models.ForeignKey(Member, on_delete=models.CASCADE)
    room_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
