from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampedModel


class TechCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Technology Categories'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Technology(TimeStampedModel):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(TechCategory, on_delete=models.CASCADE, related_name='technologies')
    image = models.ImageField(upload_to='technologies/', blank=True, null=True)
    description = models.TextField()
    applications = models.TextField(help_text='One application per line, e.g. Robotics, Automation, Sensors')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    training_level = models.CharField(max_length=150, blank=True, help_text='e.g. Secondary School to University')
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['category__order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('technologies:technology_detail', kwargs={'slug': self.slug})

    def applications_list(self):
        return [a.strip() for a in self.applications.splitlines() if a.strip()]

    def __str__(self):
        return self.name
