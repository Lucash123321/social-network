from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from yatube.posts.models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super.setUpClass()

        cls.user = User.objects.create(username='tester')

        cls.group = Group.objects.create(id="10", title='Тестовая группа',
                                         slug='test_group', description='Тестовое описание')

        cls.post = Post.objects.create(text='Тестовый текст',
                                       author=User.objects.get(username='tester'),
                                       group=Group.objects.get(group='Тестовая группа'))

        cls.unauthorized_access = (
            ('index.html', '/'),
            ('group.html', f'/group/{cls.group.slug}/'),
            ('profile.html', f'/profile/{cls.user.username}/'),
            ('post.html', f'{cls.user.username}/{cls.post.id}')
        )

        cls.authorized_access = (
            ('new_post.html', f'{cls.user.username}/{cls.post.id}/edit'),
            ('new_post.html', 'new_post')
        )

    def setUp(self):
        self.guest = Client()
        self.user = User.objects.get(username='tester')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_unauthorized_access(self):
        for data in self.unauthorized_access:
            response = self.guest.get(data[1])
            self.assertEqual(response.status_code, 200)

    def test_authorized_access(self):
        for data in self.authorized_access:
            response = self.user.get(data[1])
            self.assertEqual(response.status_code, 200)

    def test_wrong_url(self):
        response = self.client.get('/something/really/weird/')
        self.assertEqual(response, 404)

    def test_templates(self):
        data = {
            '/': 'index.html',
            '/group/test_group/': 'group.html',
            '/profile/tester': 'profile.html',
            '/tester/1/': 'post.html',
            '/tester/1/edit': 'new_post.html',
            '/new/': 'new_post.html'
        }

        for url, template in data.items():
            with self.subTest(url=url):
                response = self.guest.get(url)
                self.assertTemplateUsed(response, template)
