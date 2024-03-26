from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Receita, ReceitaTestBase


class ReceitaModelTest(ReceitaTestBase):
    def setUp(self) -> None:
        self.receita = self.make_receita()
        return super().setUp()

    def test_reciple_title_raises_error_if_title_has_more_than_65_chars(self):
        self.receita.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.receita.full_clean()

    def make_receita_no_default(self):
        receita = Receita(
            category=self.make_category(name='Teste Default Category'),
            author=self.make_author(username='newuser'),
            title='Receita Title',
            description='Receita Description',
            slug='receita-slug-for-no-default',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparations_steps='Receita Preparation Steps',
        )
        receita.full_clean()
        receita.save()
        return receita

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_receita_fields_max_lenght(self, field, max_lenght):
        setattr(self.receita, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.receita.full_clean()

    def test_receita_preparation_steps_is_html_is_false_by_default(self):
        receita = self.make_receita_no_default()
        self.assertFalse(
            receita.preparations_steps_is_html,
            msg='Receita preparation_steps_is_html is not false')

    def test_receita_is_published_is_false_by_default(self):
        receita = self.make_receita_no_default()
        self.assertFalse(
            receita.is_published,
            msg='Receita preparation_is_published is not false')

    def test_receita_string_representation(self):
        self.receita.title = 'Testing Representation'
        self.receita.full_clean()
        self.receita.save()
        self.assertEqual(str(self.receita), 'Testing Representation')
