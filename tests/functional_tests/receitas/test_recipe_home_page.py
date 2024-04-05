from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import ReceitaBaseFunctionalTest


@pytest.mark.functional_test
class ReceitaHomePageFunctionalTest(ReceitaBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😥', body.text)

    @patch('receitas.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        receitas = self.make_receita_in_batch()

        title_needed = 'This is what I need'

        receitas[0].title = title_needed
        receitas[0].save()

        # Usuario abre o browser
        self.browser.get(self.live_server_url)

        # Ve um campo de busca com o texto "Procurar por uma receita"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Procurar por uma receita"]',
        )

        # Clica nesse input e digita o termo de busca
        # para encontrar a receita com o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # O usuario vê o que estava procurando na pagina
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('receitas.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_receita_in_batch()

        # Usuario abre o browser
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na pagina 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
