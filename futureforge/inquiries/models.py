from django.db import models

from core.models import TimeStampedModel
from services.models import Service


class ContactMessage(TimeStampedModel):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.subject}'


class TrainingRequest(TimeStampedModel):
    LEVEL_CHOICES = (
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('university', 'University / College'),
        ('professional', 'Professional / Organization'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    full_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='training_requests')
    training_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    number_of_participants = models.PositiveIntegerField()
    preferred_date = models.DateField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.organization}'
