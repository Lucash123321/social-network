from django.test import TestCase, Client
from posts.models import Group, Post, User


class PostModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=User.objects.get(username='author'),
            group=Group.objects.get(title='Тестовая группа')
        )

    def setUp(self):
        self.user = Client()
        self.user.force_login(self.author)

    def test_str(self):
        self.post = Post.objects.get(id=self.post.id)
        self.assertEqual(self.post.text, str(self.post))
        self.assertEqual(self.group.title, str(self.group))
