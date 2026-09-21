from django.db import models
from django.utils.text import slugify

from core.models import TimeStampedModel
from programs.models import Program


class Institution(TimeStampedModel):
    TYPE_CHOICES = (
        ('school', 'School'),
        ('university', 'University'),
        ('college', 'College'),
        ('training_center', 'Training Center'),
        ('company', 'Company'),
        ('ngo', 'NGO'),
        ('community', 'Community Organization'),
        ('innovation_hub', 'Innovation Hub'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    logo = models.ImageField(upload_to='institutions/', blank=True, null=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    programs_conducted = models.ManyToManyField(Program, blank=True, related_name='institutions')
    partnership_info = models.TextField(blank=True, help_text='Details about the nature of the partnership')
    is_active_partner = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
