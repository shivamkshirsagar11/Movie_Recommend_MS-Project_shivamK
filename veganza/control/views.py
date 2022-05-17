from django.http import HttpResponse
from django.shortcuts import render
from control.models import Movies as m

def index(request):
    movies = m.objects.all()
    return render(request, 'index.html',{'movies':movies})
