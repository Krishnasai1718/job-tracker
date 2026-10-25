from django.http import HttpResponse

def home(request):
    return HttpResponse("Job Tracker is running!")