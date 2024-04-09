from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms.receita_form import AuthorReceitaForm
from receitas.models import Receita


class DashboardReceita(View):
    def get_receita(self, id):
        receita = None

        if id:
            receita = Receita.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not receita:
                raise Http404()

        return receita

    def render_receita(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )

    def get(self, request, id):
        receita = self.get_receita(id)
        form = AuthorReceitaForm(instance=receita)

        return self.render_receita(form)

    def post(self, request, id):
        receita = self.get_receita(id)

        form = AuthorReceitaForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=receita,
        )

        if form.is_valid():
            # Agora o form é valido e é possivel tentar salvar
            receita = form.save(commit=False)

            receita.author = request.user
            receita.preparations_steps_is_html = False
            receita.is_published = False

            receita.save()

            messages.success(request, 'Sua receita foi salva com sucesso')
            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(id,)
                        )
            )

        return self.render_receita(form)
