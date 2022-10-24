from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author3 = User.objects.create(username='author3')
        cls.group = Group.objects.create(
            title='Группа для форм',
            slug='slug',
            description='Описание группы для форм',
        )
        Post.objects.create(
            text='Пост для теста',
            author=cls.author3,
            group=cls.group,
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.author3)

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'Text'
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Text'
            ).exists()
        )

    def test_edit_post(self):

        post_id = Post.objects.filter(
            text='Пост для теста',
            group=self.group
        )[0].pk
        form_data = {
            'text': 'Пост с группой для теста',
            'group': self.group.pk
        }
        self.client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_id}),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                text='Пост с группой для теста',
            ).exists()
        )
        self.assertFalse(
            Post.objects.filter(
                text='Пост для теста',
                group=self.group
            ).exists()
        )
