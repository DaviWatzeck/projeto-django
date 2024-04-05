from django.test import TestCase

from receitas.models import Category, Receita, User


class ReceitaMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='12345',
        email='username@email.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_receita(
        self,
            category_data=None,
            author_data=None,
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
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Receita.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparations_steps=preparations_steps,
            preparations_steps_is_html=preparations_steps_is_html,
            is_published=is_published,
        )

    def make_receita_in_batch(self, qtd=10):
        receitas = []
        for i in range(qtd):
            kwargs = {
                'title': f'Título da Receita {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }
            receita = self.make_receita(**kwargs)
            receitas.append(receita)
        return receitas


class ReceitaTestBase(TestCase, ReceitaMixin):
    def setUp(self) -> None:
        return super().setUp()
