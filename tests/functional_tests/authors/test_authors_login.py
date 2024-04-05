import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # Usuario abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuario digita seu usuario e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuario envia o formulário
        form.submit()

        # Usuario ve a mensagem de login com sucesso e com seu nome
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # O Usuario abre a pagina de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # Usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Tenta enviar valores vazio
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # O usuario envia o formulario
        form.submit()

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_invalid_credentials(self):
        # O Usuario abre a pagina de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # Usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Tenta enviar valores incorretos
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('Username_Qualquer')
        password.send_keys('S3nh@_Qu@lqu3r')

        # O usuario envia o formulario
        form.submit()

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text)
