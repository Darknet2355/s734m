from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampedModel


class TeamMember(TimeStampedModel):
    full_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    position = models.CharField(max_length=150, help_text='e.g. Founder / Director, Robotics Engineer')
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    short_bio = models.CharField(max_length=300)
    full_bio = models.TextField()
    areas_of_expertise = models.TextField(help_text='One area per line')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'full_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('team:team_detail', kwargs={'slug': self.slug})

    def expertise_list(self):
        return [e.strip() for e in self.areas_of_expertise.splitlines() if e.strip()]

    def __str__(self):
        return self.full_name


class SocialLink(TimeStampedModel):
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('website', 'Website'),
    )
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f'{self.team_member.full_name} - {self.platform}'
