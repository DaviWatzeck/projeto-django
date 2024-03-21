from django.urls import resolve, reverse

from receitas import views

from .test_recipe_base import ReceitaTestBase


class ReceitaViewsTest(ReceitaTestBase):
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

    def test_receita_category_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_receita_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receita_category_template_loads_receitas(self):
        needed_title = 'Category Test'
        # Precisa de uma receita para esse teste!
        self.make_receita(title=needed_title)

        response = self.client.get(reverse('receitas:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Checa se uma receita existe
        self.assertIn(needed_title, content)

    def test_receita_detail_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:receita', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.receita)

    def test_receita_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receita_detail_template_loads_the_correct_receita(self):
        needed_title = 'Detail Test - Carrega uma receita'

        # Precisa de uma receita para esse teste!
        self.make_receita(title=needed_title)

        response = self.client.get(
            reverse('receitas:receita',
                    kwargs={'id': 1}
                    )
        )
        content = response.content.decode('utf-8')

        # Checa se uma receita existe
        self.assertIn(needed_title, content)
