from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from receitas.models import Receita
from utils.recipes.factory import make_recipe


def home(request):
    receitas = Receita.objects.filter(
        is_published=True).order_by('-id')

    return render(request, 'receitas/pages/home.html', context={
        'receitas': receitas,
    })


def category(request, category_id):
    receitas = get_list_or_404(
        Receita.objects.filter(
            category__id=category_id,
            is_published=True).order_by('-id')
    )

    return render(request, 'receitas/pages/category.html', context={
        'receitas': receitas,
        'title': f'{receitas[0].category.name} - Category | '
    })


def receita(request, id):
    receita = get_object_or_404(Receita, id=id, is_published=True,)

    return render(request, 'receitas/pages/recipe-view.html', context={
        'receita': receita,
        'is_detail_page': True,
    })
