from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('HOME 2')


def sobre(request):
    return HttpResponse('sobre 3')


def contato(request):
    return HttpResponse('contato 4')
