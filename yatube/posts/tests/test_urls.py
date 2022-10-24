from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.OK = HTTPStatus.OK
        self.NOT_FOUND = HTTPStatus.NOT_FOUND
        self.guest = Client()
        self.user = Client()
        self.user2 = Client()
        user = User.objects.create_user(username='Unknown')
        user2 = User.objects.create_user(username='Unknown2')
        self.user.force_login(user)
        self.user2.force_login(user2)
        Post.objects.create(
            text='Текст поста',
            author=user2,
            pk=2)
        Post.objects.create(
            text='Текст поста',
            author=user,
            pk=1)
        Group.objects.create(
            title='Группа',
            slug='slug',
            description='Группа')

    def test_404(self):
        """Выбрасывает 404 при запросе на несуществующую страницу"""
        fake_response = self.guest.get('/unexisting_page/')
        self.assertEqual(fake_response.status_code, self.NOT_FOUND)

    def test_302(self):
        """Редирект гостей на вход"""
        guest_create_response = self.guest.get('/create/')
        self.assertRedirects(guest_create_response,
                             ('/auth/login/?next=/create/'))

        guest_edit_response = self.guest.get('/posts/1/edit/')
        self.assertRedirects(guest_edit_response,
                             ('/auth/login/?next=/posts/1/edit/'))

        """Редирект при попытке редактирования чужого поста"""
        user_edit_other_response = self.user.get('/posts/2/edit/')
        self.assertRedirects(user_edit_other_response, ('/posts/2/'))

    def test_200(self):
        def subTester(dictionary, user_guest):
            for address, template in dictionary.items():
                with self.subTest(address=address):
                    response = user_guest.get(address)
                    self.assertEqual(response.status_code, self.OK)
                    self.assertTemplateUsed(response, template)
        """200 для авторизированных юзеров"""
        urls_templates_names_users = {
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html'
        }
        """Все 200 для гостей"""
        urls_templates_names_guests = {
            '/': 'posts/index.html',
            '/group/slug/': 'posts/group_list.html',
            '/profile/Unknown/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html'
        }

        subTester(urls_templates_names_guests, self.guest)
        subTester(urls_templates_names_users, self.user)
