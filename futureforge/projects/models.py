from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampedModel
from technologies.models import Technology


class Project(TimeStampedModel):
    CATEGORY_CHOICES = (
        ('robotics', 'Robotics'),
        ('ai', 'Artificial Intelligence'),
        ('iot', 'Internet of Things'),
        ('electronics', 'Electronics'),
        ('automation', 'Automation'),
        ('school_innovation', 'School Innovation'),
    )
    AUDIENCE_CHOICES = (
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('university', 'University / College'),
        ('professional', 'Professional / Organizations'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    featured_image = models.ImageField(upload_to='projects/featured/')
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name='projects', blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)
    video_url = models.URLField(blank=True, help_text='Optional YouTube link')
    project_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-project_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.project.title} - image {self.id}'
