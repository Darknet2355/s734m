from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.models import BlogPost
from inquiries.models import ContactMessage, TrainingRequest
from institutions.models import Institution
from media_gallery.models import MediaItem
from programs.models import Program
from projects.models import Project
from services.models import Service
from team.models import TeamMember
from technologies.models import Technology

from .forms import (
    BlogPostForm, InstitutionForm, MediaItemForm, ProgramForm, ProjectForm,
    ServiceForm, TeamMemberForm, TechnologyForm, TrainingRequestStatusForm,
)

PAGINATE_BY = 10


# =====================================================================
# Dashboard home
# =====================================================================
@login_required(login_url='accounts:admin_login')
def index(request):
    context = {
        'stats': {
            'total_programs': Program.objects.count(),
            'total_technologies': Technology.objects.count(),
            'total_projects': Project.objects.count(),
            'total_institutions': Institution.objects.count(),
            'total_team_members': TeamMember.objects.count(),
            'published_posts': BlogPost.objects.filter(status='published').count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'pending_requests': TrainingRequest.objects.filter(status='pending').count(),
        },
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'recent_requests': TrainingRequest.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/index.html', context)


# =====================================================================
# Generic mixins for consistent CRUD behavior across every model
# =====================================================================
class DashCreateView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/generic_form.html'
    login_url = 'accounts:admin_login'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{self.model_label} created successfully.')
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = f'Add {self.model_label}'
        ctx['cancel_url'] = self.success_url
        return ctx


class DashUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/generic_form.html'
    login_url = 'accounts:admin_login'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{self.model_label} updated successfully.')
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = f'Edit {self.model_label}'
        ctx['cancel_url'] = self.success_url
        return ctx


class DashDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/generic_confirm_delete.html'
    login_url = 'accounts:admin_login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['model_label'] = self.model_label
        ctx['cancel_url'] = self.success_url
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'{self.model_label} deleted.')
        return super().form_valid(form)


# =====================================================================
# Programs
# =====================================================================
class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    template_name = 'dashboard/programs/list.html'
    context_object_name = 'programs'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = Program.objects.select_related('category').all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class ProgramCreateView(DashCreateView):
    model = Program
    form_class = ProgramForm
    model_label = 'Program'
    success_url = reverse_lazy('dashboard:program_list')


class ProgramUpdateView(DashUpdateView):
    model = Program
    form_class = ProgramForm
    model_label = 'Program'
    success_url = reverse_lazy('dashboard:program_list')


class ProgramDeleteView(DashDeleteView):
    model = Program
    model_label = 'Program'
    success_url = reverse_lazy('dashboard:program_list')


# =====================================================================
# Technologies
# =====================================================================
class TechnologyListView(LoginRequiredMixin, ListView):
    model = Technology
    template_name = 'dashboard/technologies/list.html'
    context_object_name = 'technologies'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = Technology.objects.select_related('category').all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs


class TechnologyCreateView(DashCreateView):
    model = Technology
    form_class = TechnologyForm
    model_label = 'Technology'
    success_url = reverse_lazy('dashboard:technology_list')


class TechnologyUpdateView(DashUpdateView):
    model = Technology
    form_class = TechnologyForm
    model_label = 'Technology'
    success_url = reverse_lazy('dashboard:technology_list')


class TechnologyDeleteView(DashDeleteView):
    model = Technology
    model_label = 'Technology'
    success_url = reverse_lazy('dashboard:technology_list')


# =====================================================================
# Institutions
# =====================================================================
class InstitutionListView(LoginRequiredMixin, ListView):
    model = Institution
    template_name = 'dashboard/institutions/list.html'
    context_object_name = 'institutions'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = Institution.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(location__icontains=q))
        return qs


class InstitutionCreateView(DashCreateView):
    model = Institution
    form_class = InstitutionForm
    model_label = 'Institution'
    success_url = reverse_lazy('dashboard:institution_list')


class InstitutionUpdateView(DashUpdateView):
    model = Institution
    form_class = InstitutionForm
    model_label = 'Institution'
    success_url = reverse_lazy('dashboard:institution_list')


class InstitutionDeleteView(DashDeleteView):
    model = Institution
    model_label = 'Institution'
    success_url = reverse_lazy('dashboard:institution_list')


# =====================================================================
# Projects
# =====================================================================
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'dashboard/projects/list.html'
    context_object_name = 'projects'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = Project.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class ProjectCreateView(DashCreateView):
    model = Project
    form_class = ProjectForm
    model_label = 'Project'
    success_url = reverse_lazy('dashboard:project_list')


class ProjectUpdateView(DashUpdateView):
    model = Project
    form_class = ProjectForm
    model_label = 'Project'
    success_url = reverse_lazy('dashboard:project_list')


class ProjectDeleteView(DashDeleteView):
    model = Project
    model_label = 'Project'
    success_url = reverse_lazy('dashboard:project_list')


# =====================================================================
# Services
# =====================================================================
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'dashboard/services/list.html'
    context_object_name = 'services'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = Service.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs


class ServiceCreateView(DashCreateView):
    model = Service
    form_class = ServiceForm
    model_label = 'Service'
    success_url = reverse_lazy('dashboard:service_list')


class ServiceUpdateView(DashUpdateView):
    model = Service
    form_class = ServiceForm
    model_label = 'Service'
    success_url = reverse_lazy('dashboard:service_list')


class ServiceDeleteView(DashDeleteView):
    model = Service
    model_label = 'Service'
    success_url = reverse_lazy('dashboard:service_list')


# =====================================================================
# Team
# =====================================================================
class TeamListView(LoginRequiredMixin, ListView):
    model = TeamMember
    template_name = 'dashboard/team/list.html'
    context_object_name = 'members'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = TeamMember.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(position__icontains=q))
        return qs


class TeamCreateView(DashCreateView):
    model = TeamMember
    form_class = TeamMemberForm
    model_label = 'Team Member'
    success_url = reverse_lazy('dashboard:team_list')


class TeamUpdateView(DashUpdateView):
    model = TeamMember
    form_class = TeamMemberForm
    model_label = 'Team Member'
    success_url = reverse_lazy('dashboard:team_list')


class TeamDeleteView(DashDeleteView):
    model = TeamMember
    model_label = 'Team Member'
    success_url = reverse_lazy('dashboard:team_list')


# =====================================================================
# Blog
# =====================================================================
class BlogListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'dashboard/blog/list.html'
    context_object_name = 'posts'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = BlogPost.objects.select_related('category', 'author').all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class BlogCreateView(DashCreateView):
    model = BlogPost
    form_class = BlogPostForm
    model_label = 'Blog Post'
    success_url = reverse_lazy('dashboard:blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(DashUpdateView):
    model = BlogPost
    form_class = BlogPostForm
    model_label = 'Blog Post'
    success_url = reverse_lazy('dashboard:blog_list')


class BlogDeleteView(DashDeleteView):
    model = BlogPost
    model_label = 'Blog Post'
    success_url = reverse_lazy('dashboard:blog_list')


@login_required(login_url='accounts:admin_login')
def blog_toggle_publish(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.status = 'draft' if post.status == 'published' else 'published'
    if post.status == 'published' and not post.published_at:
        post.published_at = timezone.now()
    post.save()
    messages.success(request, f'"{post.title}" is now {post.get_status_display()}.')
    return redirect('dashboard:blog_list')


# =====================================================================
# Media
# =====================================================================
class MediaListView(LoginRequiredMixin, ListView):
    model = MediaItem
    template_name = 'dashboard/media/list.html'
    context_object_name = 'items'
    paginate_by = PAGINATE_BY
    login_url = 'accounts:admin_login'

    def get_queryset(self):
        qs = MediaItem.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q))
        return qs


class MediaCreateView(DashCreateView):
    model = MediaItem
    form_class = MediaItemForm
    model_label = 'Media Item'
    success_url = reverse_lazy('dashboard:media_list')


class MediaUpdateView(DashUpdateView):
    model = MediaItem
    form_class = MediaItemForm
    model_label = 'Media Item'
    success_url = reverse_lazy('dashboard:media_list')


class MediaDeleteView(DashDeleteView):
    model = MediaItem
    model_label = 'Media Item'
    success_url = reverse_lazy('dashboard:media_list')


# =====================================================================
# Messages (contact form submissions)
# =====================================================================
@login_required(login_url='accounts:admin_login')
def message_list(request):
    qs = ContactMessage.objects.all()
    status = request.GET.get('status')
    if status == 'unread':
        qs = qs.filter(is_read=False)
    elif status == 'read':
        qs = qs.filter(is_read=True)
    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(full_name__icontains=q) | Q(subject__icontains=q) | Q(email__icontains=q))

    page_obj = Paginator(qs, PAGINATE_BY).get_page(request.GET.get('page'))
    return render(request, 'dashboard/messages/list.html', {'page_obj': page_obj, 'active_status': status})


@login_required(login_url='accounts:admin_login')
def message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    return redirect('dashboard:message_list')


@login_required(login_url='accounts:admin_login')
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
        return redirect('dashboard:message_list')
    return render(request, 'dashboard/messages/confirm_delete.html', {'msg': msg})


# =====================================================================
# Training Requests
# =====================================================================
@login_required(login_url='accounts:admin_login')
def training_request_list(request):
    qs = TrainingRequest.objects.select_related('service').all()
    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)
    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(full_name__icontains=q) | Q(organization__icontains=q))

    page_obj = Paginator(qs, PAGINATE_BY).get_page(request.GET.get('page'))
    return render(request, 'dashboard/requests/list.html', {
        'page_obj': page_obj,
        'active_status': status,
        'status_choices': TrainingRequest.STATUS_CHOICES,
    })


@login_required(login_url='accounts:admin_login')
def training_request_update_status(request, pk):
    req_obj = get_object_or_404(TrainingRequest, pk=pk)
    if request.method == 'POST':
        form = TrainingRequestStatusForm(request.POST, instance=req_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Status updated to {req_obj.get_status_display()}.')
    return redirect('dashboard:training_request_list')


@login_required(login_url='accounts:admin_login')
def training_request_delete(request, pk):
    req_obj = get_object_or_404(TrainingRequest, pk=pk)
    if request.method == 'POST':
        req_obj.delete()
        messages.success(request, 'Training request deleted.')
        return redirect('dashboard:training_request_list')
    return render(request, 'dashboard/requests/confirm_delete.html', {'req_obj': req_obj})


# =====================================================================
# Global dashboard search
# =====================================================================
@login_required(login_url='accounts:admin_login')
def global_search(request):
    query = request.GET.get('q', '').strip()
    results = {}
    if query:
        results['Programs'] = [
            (p.title, reverse('dashboard:program_edit', args=[p.pk]))
            for p in Program.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:10]
        ]
        results['Technologies'] = [
            (t.name, reverse('dashboard:technology_edit', args=[t.pk]))
            for t in Technology.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:10]
        ]
        results['Institutions'] = [
            (i.name, reverse('dashboard:institution_edit', args=[i.pk]))
            for i in Institution.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))[:10]
        ]
        results['Projects'] = [
            (p.title, reverse('dashboard:project_edit', args=[p.pk]))
            for p in Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:10]
        ]
        results['Services'] = [
            (s.title, reverse('dashboard:service_edit', args=[s.pk]))
            for s in Service.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:10]
        ]
        results['Team Members'] = [
            (m.full_name, reverse('dashboard:team_edit', args=[m.pk]))
            for m in TeamMember.objects.filter(Q(full_name__icontains=query) | Q(position__icontains=query))[:10]
        ]
        results['Blog Posts'] = [
            (b.title, reverse('dashboard:blog_edit', args=[b.pk]))
            for b in BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))[:10]
        ]
        results['Media Items'] = [
            (m.title, reverse('dashboard:media_edit', args=[m.pk]))
            for m in MediaItem.objects.filter(Q(title__icontains=query))[:10]
        ]
        results['Messages'] = [
            (f'{m.full_name} — {m.subject}', reverse('dashboard:message_list') + f'?q={m.full_name}')
            for m in ContactMessage.objects.filter(Q(full_name__icontains=query) | Q(subject__icontains=query) | Q(email__icontains=query))[:10]
        ]
        results['Training Requests'] = [
            (f'{t.full_name} — {t.organization}', reverse('dashboard:training_request_list') + f'?q={t.full_name}')
            for t in TrainingRequest.objects.filter(Q(full_name__icontains=query) | Q(organization__icontains=query))[:10]
        ]
    total_results = sum(len(v) for v in results.values())
    return render(request, 'dashboard/search_results.html', {
        'query': query, 'results': results, 'total_results': total_results,
    })
