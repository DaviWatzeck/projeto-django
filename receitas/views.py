from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'receitas/home.html')


def sobre(request):
    return HttpResponse('sobre 3')


def contato(request):
    return HttpResponse('contato 4')
