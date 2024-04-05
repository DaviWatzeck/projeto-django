from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        string_password = 'My_P@ss'
        string_username = 'My_User'
        User.objects.create_user(
            username=string_username, password=string_password)
        self.client.login(username=string_username, password=string_password)

        response = self.client.get(
            reverse('authors:logout'),
            follow=True,
        )

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8'),
        )

    def test_user_tries_to_logout_another_user(self):
        string_password = 'My_P@ss'
        string_username = 'My_User'
        User.objects.create_user(
            username=string_username, password=string_password)
        self.client.login(username=string_username, password=string_password)

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'outro_usuario',
                'password': 'outra_senha'
            },
            follow=True,
        )

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8'),
        )

    def test_user_can_logout_successfully(self):
        string_password = 'My_P@ss'
        string_username = 'My_User'
        User.objects.create_user(
            username=string_username, password=string_password)
        self.client.login(username=string_username, password=string_password)

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': string_username,
                'password': string_password
            },
            follow=True,
        )

        self.assertIn(
            'Logged out successfully',
            response.content.decode('utf-8'),
        )
