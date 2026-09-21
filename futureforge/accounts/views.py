from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AdminLoginForm


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'Welcome back, {request.user.get_full_name() or request.user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'dashboard:index')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='accounts:admin_login')
def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')
