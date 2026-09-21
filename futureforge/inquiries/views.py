from django.contrib import messages
from django.shortcuts import redirect, render

from services.models import Service

from .forms import ContactMessageForm, TrainingRequestForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Your message has been sent. Our team will get back to you shortly."
            )
            return redirect('inquiries:contact')
        messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})


def training_request_view(request):
    initial = {}
    service_slug = request.GET.get('service')
    if service_slug:
        service_obj = Service.objects.filter(slug=service_slug, is_active=True).first()
        if service_obj:
            initial['service'] = service_obj.pk

    if request.method == 'POST':
        form = TrainingRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your training request has been submitted! Our team will contact you soon to "
                "confirm the schedule."
            )
            return redirect('inquiries:training_request')
        messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = TrainingRequestForm(initial=initial)

    return render(request, 'training_request.html', {'form': form})
