import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from receitas.models import Receita
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class ReceitaListViewBase(ListView):
    model = Receita
    context_object_name = 'receitas'
    ordering = ['-id']
    template_name = 'receitas/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('receitas'),
            PER_PAGE
        )
        ctx.update(
            {'receitas': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class ReceitaListViewHome(ReceitaListViewBase):
    template_name = 'receitas/pages/home.html'


class ReceitaListViewCategory(ReceitaListViewBase):
    template_name = 'receitas/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("receitas")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class ReceitaListViewSearch(ReceitaListViewBase):
    template_name = 'receitas/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })
        return ctx


def receita(request, id):
    receita = get_object_or_404(Receita, id=id, is_published=True,)

    return render(request, 'receitas/pages/recipe-view.html', context={
        'receita': receita,
        'is_detail_page': True,
    })


class ReceitaDetail(DetailView):
    model = Receita
    context_object_name = 'receita'
    template_name = 'receitas/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'is_detail_page': True,
        })

        return ctx
