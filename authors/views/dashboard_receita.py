from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.receita_form import AuthorReceitaForm
from receitas.models import Receita


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardReceita(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_receita(self, id=None):
        receita = None

        if id is not None:
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

    def get(self, request, id=None):
        receita = self.get_receita(id)
        form = AuthorReceitaForm(instance=receita)

        return self.render_receita(form)

    def post(self, request, id=None):
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
                reverse('authors:dashboard_recipe_edit', args=(receita.id,)
                        )
            )

        return self.render_receita(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardReceitaDelete(DashboardReceita):
    def post(self, *args, **kwargs):
        receita = self.get_receita(self.request.POST.get('id'))
        receita.delete()
        messages.success(self.request, 'Deleted with successfully')
        return redirect(reverse('authors:dashboard'))
