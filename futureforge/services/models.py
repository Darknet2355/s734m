from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampedModel


class Service(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    icon_class = models.CharField(
        max_length=100, blank=True,
        help_text='Font Awesome icon class, e.g. "fa-solid fa-robot"'
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    description = models.TextField()
    target_clients = models.TextField(help_text='One client type per line, e.g. Schools, Companies, NGOs')
    benefits = models.TextField(help_text='One benefit per line')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})

    def target_clients_list(self):
        return [c.strip() for c in self.target_clients.splitlines() if c.strip()]

    def benefits_list(self):
        return [b.strip() for b in self.benefits.splitlines() if b.strip()]

    def __str__(self):
        return self.title
