from django.urls import resolve, reverse

from receitas import views

from .test_recipe_base import ReceitaTestBase


class ReceitaSearchViewTest(ReceitaTestBase):
    def test_receita_search_uses_correct_view_functionI(self):
        resolved = resolve(reverse('receitas:search'))
        self.assertIs(resolved.func.view_class, views.ReceitaListViewSearch),

    def teste_receit_search_loads_correct_template(self):
        response = self.client.get(reverse('receitas:search') + '?q=teste')
        self.assertTemplateUsed(response, 'receitas/pages/search.html')

    def teste_receita_search_raises_404_if_no_search_term(self):
        url = reverse('receitas:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_receita_search_term_is_on_page_title_and_escaped(self):
        url = reverse('receitas:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )

    def test_receita_search_can_find_receita_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        receita1 = self.make_receita(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        receita2 = self.make_receita(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('receitas:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(receita1, response1.context['receitas'])
        self.assertNotIn(receita2, response1.context['receitas'])

        self.assertIn(receita2, response2.context['receitas'])
        self.assertNotIn(receita1, response2.context['receitas'])

        self.assertIn(receita1, response_both.context['receitas'])
        self.assertIn(receita2, response_both.context['receitas'])
