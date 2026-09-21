from django import forms

from .models import ContactMessage, TrainingRequest


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+256 700 000 000 (optional)'}),
            'subject': forms.TextInput(attrs={'placeholder': 'How can we help?'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your message...', 'rows': 5}),
        }

    def clean_full_name(self):
        name = self.cleaned_data['full_name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Please enter your full name.')
        return name


class TrainingRequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = [
            'full_name', 'organization', 'email', 'phone_number', 'location',
            'service', 'training_level', 'number_of_participants', 'preferred_date', 'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'organization': forms.TextInput(attrs={'placeholder': 'School / institution / company'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+256 700 000 000'}),
            'location': forms.TextInput(attrs={'placeholder': 'City / District'}),
            'number_of_participants': forms.NumberInput(attrs={'min': 1, 'placeholder': 'e.g. 30'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us more about your training needs (optional)'}),
        }

    def clean_number_of_participants(self):
        value = self.cleaned_data['number_of_participants']
        if value < 1:
            raise forms.ValidationError('Number of participants must be at least 1.')
        return value
