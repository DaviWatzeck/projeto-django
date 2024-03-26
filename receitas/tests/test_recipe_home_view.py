from django.urls import resolve, reverse

from receitas import views

from .test_recipe_base import ReceitaTestBase


class ReceitaHomeViewTest(ReceitaTestBase):
    def test_receita_home_view_function_is_correct(self):
        view = resolve(reverse('receitas:home'))
        self.assertIs(view.func, views.home)

    def test_receita_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code, 200)

    def test_receita_home_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response, 'receitas/pages/home.html')

    def test_receita_home_template_shows_no_receitas_found_if_no_recipe(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertIn(
            '<h1> No recipes found here 😥<h1>',
            response.content.decode('utf-8')
        )

    def test_receita_home_template_loads_receitas(self):
        self.make_receita()

        response = self.client.get(reverse('receitas:home'))
        content = response.content.decode('utf-8')
        response_context_receitas = response.context['receitas']

        # Checa se uma receita existe
        self.assertIn('Receita Title', content)
        self.assertEqual(len(response_context_receitas), 1)

    def test_receita_home_template_dont_load_recipes_not_published(self):
        """
        Testa se a receita está publicada, se for false, não mostra
        """
        self.make_receita(is_published=False)

        response = self.client.get(reverse('receitas:home'))

        # Checa se uma receita existe
        self.assertIn(
            '<h1> No recipes found here 😥<h1>',
            response.content.decode('utf-8')
        )
