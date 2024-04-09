from django.urls import resolve, reverse

from receitas import views

from .test_recipe_base import ReceitaTestBase


class ReceitaDetailViewTest(ReceitaTestBase):
    def test_receita_detail_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:receita', kwargs={'pk': 1})
        )
        self.assertIs(view.func.view_class, views.ReceitaDetail)

    def test_receita_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receita_detail_template_loads_the_correct_receita(self):
        needed_title = 'Detail Test - Carrega uma receita'

        self.make_receita(title=needed_title)

        response = self.client.get(
            reverse('receitas:receita',
                    kwargs={'pk': 1}
                    )
        )
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_receita_detail_template_dont_load_recipe_not_published(self):
        """
        Testa se a receita está publicada, se for false, não mostra
        """

        receita = self.make_receita(is_published=False)

        response = self.client.get(
            reverse(
                'receitas:receita',
                kwargs={
                    'pk': receita.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
