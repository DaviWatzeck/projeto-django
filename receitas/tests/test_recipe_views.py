from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from receitas import views
from receitas.models import Category, Receita


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

    def test_receita_home_template_shows_no_receitas_found_if_no_recipe(self):
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

    def test_receita_home_template_loads_receitas(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='12345',
            email='username@email.com'
        )
        receita = Receita.objects.create(
            category=category,
            author=author,
            title='Receita Title',
            description='Receita Description',
            slug='receita-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparations_steps='Receita Preparation Steps',
            preparations_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse('receitas:home'))
        content = response.content.decode('utf-8')
        response_context_receitas = response.context['receitas']

        self.assertIn('Receita Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_receitas), 1)
