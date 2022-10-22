from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest = Client()
        self.OK: int = HTTPStatus.OK
        self.NOT_FOUND = HTTPStatus.NOT_FOUND

    def test_200(self):

        def subTester(dictionary, user_guest):
            for address, template in dictionary.items():
                with self.subTest(address=address):
                    response = user_guest.get(address)
                    self.assertEqual(response.status_code, self.OK)
                    if template:
                        self.assertTemplateUsed(response, template)

        """Все 200 для гостей"""
        urls_templates_names_guests = {
            '/auth/signup/': None,
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': None
        }
        
        subTester(urls_templates_names_guests, self.guest)

    def test_404(self):
        fake_response = self.guest.get('auth/how_to_test_urls/')
        self.assertEqual(fake_response.status_code, self.NOT_FOUND)
