# Create your views here.
from django.shortcuts import render
from django.template import loader


# Главная страница
def index(request):
    template = 'works/index.html'
    return render(request, template)
