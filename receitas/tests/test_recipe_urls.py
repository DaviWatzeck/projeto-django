from django.test import TestCase
from django.urls import reverse


class ReceitaURLsTest(TestCase):
    def test_receita_home_urls_is_correct(self):
        url = reverse('receitas:home')
        self.assertEqual(url, '/')

    def test_receita_category_urls_is_correct(self):
        url = reverse('receitas:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/receitas/category/1/')

    def test_receita_receita_urls_is_correct(self):
        url = reverse('receitas:receita', kwargs={'pk': 1})
        self.assertEqual(url, '/receitas/1/')

    def test_receita_search_url_is_correct(self):
        url = reverse('receitas:search')
        self.assertEqual(url, '/receitas/search/')
