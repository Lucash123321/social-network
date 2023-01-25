from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username='tester')

        cls.group = Group.objects.create(id="10", title='Тестовая группа',
                                         slug='test_group', description='Тестовое описание')

        cls.post = Post.objects.create(text='Тестовый текст',
                                       author=User.objects.get(username='tester'),
                                       group=Group.objects.get(title='Тестовая группа'))

        cls.unauthorized_access = (
            ('posts/index.html', '/'),
            ('posts/group_posts.html', f'/group/{cls.group.slug}/'),
            ('posts/profile.html', f'/profile/{cls.user.username}/'),
            ('posts/view_post.html', f'/posts/{cls.post.id}')
        )

        cls.authorized_access = (
            ('posts/create_post.html', f'/posts/{cls.post.id}/edit/'),
            ('posts/create_post.html', '/create/')
        )

    def setUp(self):
        self.guest = Client()
        self.user = User.objects.get(username='tester')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_unauthorized_access(self):
        with self.subTest(True):
            for data in self.unauthorized_access:
                response = self.guest.get(data[1], follow=True)
                self.assertEqual(response.status_code, 200)

    def test_authorized_access(self):
        for data in self.authorized_access:
            response = self.authorized_client.get(data[1])
            self.assertEqual(response.status_code, 200)

    def test_wrong_url(self):
        response = self.client.get('/something/really/weird/')
        self.assertEqual(response.status_code, 404)

    def test_templates(self):
        data = {
            '/': 'posts/index.html',
            '/group/test_group/': 'posts/group_posts.html',
            '/profile/tester/': 'posts/profile.html',
            '/posts/1/': 'posts/view_post.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html'
        }

        for url, template in data.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
