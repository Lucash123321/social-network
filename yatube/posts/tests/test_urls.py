from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Group, Post, User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='tester')

        cls.group = Group.objects.create(title='Тестовая группа',
                                         slug='test_group',
                                         description='Тестовое описание')

        cls.post = Post.objects.create(text='Тестовый текст',
                                       author=User.objects.get(username='tester'),
                                       group=Group.objects.get(title='Тестовая группа'))

        cls.unauthorized_access = (
            '/',
            f'/group/{cls.group.slug}/',
            f'/profile/{cls.user.username}/',
            f'/posts/{cls.post.id}',
            '/about/author/',
            '/about/tech/'
        )

        cls.authorized_access = {
            f'/posts/{cls.post.id}/edit/': f'/auth/login/?next=/posts/{cls.post.id}/edit/',
            '/create/': '/auth/login/?next=/create/'
        }

        cls.sites = {
            '/': 'posts/index.html',
            f'/group/{cls.group.slug}/': 'posts/group_posts.html',
            f'/profile/{cls.user.username}/': 'posts/profile.html',
            f'/posts/{cls.post.id}/': 'posts/view_post.html',
            f'/posts/{cls.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }

    def setUp(self):
        self.guest = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_unauthorized_access(self):
        with self.subTest(True):
            for url in self.unauthorized_access:
                response = self.guest.get(url, follow=True)
                self.assertEqual(response.status_code, 200)

    def test_authorized_access(self):
        for url in self.sites.keys():
            with self.subTest(True):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_redirection(self):
        for url, redirection in self.authorized_access.items():
            with self.subTest(True):
                response = self.guest.get(url, follow=True)
                self.assertRedirects(response, redirection)

    def test_wrong_url(self):
        response = self.client.get('/something/really/weird/')
        self.assertEqual(response.status_code, 404)

    def test_templates(self):
        for url, template in self.sites.items():
            with self.subTest(True):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
