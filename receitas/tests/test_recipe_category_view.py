from django.urls import resolve, reverse

from receitas import views

from .test_recipe_base import ReceitaTestBase


class ReceitaCategoryViewTest(ReceitaTestBase):
    def test_receita_category_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func.view_class, views.ReceitaListViewCategory)

    def test_receita_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receita_category_template_loads_receitas(self):
        needed_title = 'Category Test'
        # Precisa de uma receita para esse teste e cria um titulo para testar
        self.make_receita(title=needed_title)

        response = self.client.get(reverse('receitas:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Checa se o titulo da receita existe
        self.assertIn(needed_title, content)

    def test_receita_category_template_dont_load_recipes_not_published(self):
        """
        Testa se a receita está publicada, se for false, não mostra
        """

        receita = self.make_receita(is_published=False)

        response = self.client.get(
            reverse('receitas:receita', kwargs={'pk': receita.category.id}))

        self.assertEqual(response.status_code, 404)
