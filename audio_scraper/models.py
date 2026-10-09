import os

from django.db import models
from django.utils.timezone import now
from django.conf import settings

def audio_upload_path(instance, filename):
    return os.path.join("audios", instance.category, filename)

class AudioContent(models.Model):
    CATEGORY_CHOICES = [
        ('Hausa', 'Hausa'),
        ('Igbo', 'Igbo'),
        ('Yoruba', 'Yoruba'),
        ('Efik', 'Efik'),
        ('Tiv', 'Tiv'),
    ]

    title = models.CharField(max_length=225)
    content_link = models.URLField()
    audio_file = models.FileField(upload_to=audio_upload_path, blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, str(self.audio_file))
        if os.path.exists(file_path):
            os.remove(file_path)
        
        category_folder = os.path.dirname(file_path)
        if os.path.exists(category_folder) and not os.listdir(category_folder):
            os.rmdir(category_folder)

        super().delete(*args, **kwargs)
