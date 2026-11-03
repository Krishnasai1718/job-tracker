from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q                                 # CHANGED: new import
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application


@login_required
def application_list(request):                                   # CHANGED: whole function
    applications = Application.objects.filter(user=request.user)

    status = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()

    if status:
        applications = applications.filter(status=status)
    if query:
        applications = applications.filter(
            Q(company__icontains=query) | Q(role__icontains=query)
        )

    applications = applications.order_by('-applied_date')

    context = {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
        'selected_status': status,
        'query': query,
    }
    return render(request, 'applications/application_list.html', context)


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('application_list')
    else:
        form = ApplicationForm()
    return render(request, 'applications/application_form.html', {'form': form, 'title': 'Add Application'})


@login_required
def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_list')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'applications/application_form.html', {'form': form, 'title': 'Edit Application'})


@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        application.delete()
        return redirect('application_list')
    return render(request, 'applications/application_confirm_delete.html', {'application': application})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('application_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    qs = Application.objects.filter(user=request.user)
    counts = dict(qs.values_list('status').annotate(total=Count('id')))

    stats = [
        {'value': value, 'label': label, 'count': counts.get(value, 0)}
        for value, label in Application.STATUS_CHOICES
    ]
    chart_data = {
        'labels': [s['label'] for s in stats],
        'data': [s['count'] for s in stats],
    }
    context = {
        'stats': stats,
        'total': sum(s['count'] for s in stats),
        'chart_data': chart_data,
    }
    return render(request, 'applications/dashboard.html', context)