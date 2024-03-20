from django.test import TestCase
from django.urls import resolve, reverse

from receitas import views


class ReceitaViewsTest(TestCase):
    def test_receita_home_view_function_is_correct(self):
        view = resolve(reverse('receitas:home'))
        self.assertIs(view.func, views.home)

    def test_receita_category_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_receita_detail_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:receita', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.receita)

    def test_receita_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code, 200)

    def test_receita_home_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response, 'receitas/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertIn(
            '<h1> No recipes found here 😥<h1>',
            response.content.decode('utf-8')
        )

    def test_receita_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receita_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
