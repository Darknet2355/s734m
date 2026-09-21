from django import forms

from blog.models import BlogPost
from inquiries.models import TrainingRequest
from institutions.models import Institution
from media_gallery.models import MediaItem
from programs.models import Program
from projects.models import Project
from services.models import Service
from team.models import TeamMember
from technologies.models import Technology


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'title', 'category', 'image', 'description', 'target_audience',
            'duration', 'skills_acquired', 'difficulty_level', 'status', 'is_featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'skills_acquired': forms.Textarea(attrs={'rows': 4, 'placeholder': 'One skill per line'}),
        }


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = [
            'name', 'category', 'image', 'description', 'applications',
            'difficulty', 'training_level', 'is_featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'applications': forms.Textarea(attrs={'rows': 4, 'placeholder': 'One application per line'}),
        }


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = [
            'name', 'logo', 'type', 'location', 'description',
            'programs_conducted', 'partnership_info', 'is_active_partner',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'partnership_info': forms.Textarea(attrs={'rows': 3}),
            'programs_conducted': forms.CheckboxSelectMultiple,
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'featured_image', 'description', 'technologies', 'category',
            'target_audience', 'video_url', 'project_date', 'status', 'is_featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'technologies': forms.CheckboxSelectMultiple,
            'project_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title', 'icon_class', 'image', 'description',
            'target_clients', 'benefits', 'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'target_clients': forms.Textarea(attrs={'rows': 3, 'placeholder': 'One client type per line'}),
            'benefits': forms.Textarea(attrs={'rows': 3, 'placeholder': 'One benefit per line'}),
            'icon_class': forms.TextInput(attrs={'placeholder': 'e.g. fa-solid fa-robot'}),
        }


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            'full_name', 'position', 'photo', 'short_bio',
            'full_bio', 'areas_of_expertise', 'order', 'is_active',
        ]
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 2}),
            'full_bio': forms.Textarea(attrs={'rows': 6}),
            'areas_of_expertise': forms.Textarea(attrs={'rows': 3, 'placeholder': 'One area per line'}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'featured_image', 'category', 'tags', 'excerpt', 'content', 'status']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 10}),
            'tags': forms.CheckboxSelectMultiple,
        }


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'media_type', 'category', 'image', 'video_url', 'description', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'video_url': forms.URLInput(attrs={'placeholder': 'Required for video items — YouTube embed URL'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('media_type') == 'video' and not cleaned.get('video_url'):
            self.add_error('video_url', 'A video URL is required for video media items.')
        if cleaned.get('media_type') == 'image' and not cleaned.get('image') and not self.instance.pk:
            self.add_error('image', 'An image is required for image media items.')
        return cleaned


class TrainingRequestStatusForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['status']
