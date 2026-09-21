from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampedModel


class ProgramCategory(TimeStampedModel):
    """Primary School / Secondary School / University-College / Professional-Organizations."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Program Categories'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Program(TimeStampedModel):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('coming_soon', 'Coming Soon'),
        ('archived', 'Archived'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, related_name='programs')
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    description = models.TextField()
    target_audience = models.CharField(max_length=255, help_text='e.g. Ages 10-14, Grade 7-9 students')
    duration = models.CharField(max_length=100, help_text='e.g. 6 weeks, 3 days intensive')
    skills_acquired = models.TextField(help_text='One skill per line')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['category__order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('programs:program_detail', kwargs={'slug': self.slug})

    def skills_list(self):
        return [s.strip() for s in self.skills_acquired.splitlines() if s.strip()]

    def __str__(self):
        return self.title
