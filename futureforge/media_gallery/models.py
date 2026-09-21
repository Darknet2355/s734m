from django.db import models

from core.models import TimeStampedModel


class MediaItem(TimeStampedModel):
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video (YouTube)'),
    )
    CATEGORY_CHOICES = (
        ('robotics', 'Robotics'),
        ('arduino', 'Arduino'),
        ('programming', 'Programming'),
        ('ai', 'Artificial Intelligence'),
        ('electronics', 'Electronics'),
        ('projects', 'Projects'),
        ('training', 'Training'),
        ('events', 'Events'),
    )

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='YouTube URL — required if media type is Video')
    description = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
