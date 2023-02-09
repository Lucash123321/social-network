from django.test import Client, TestCase
from posts.models import Group, Post, User, Follow, Comment
from django.urls import reverse


class PostFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')

        cls.follower = User.objects.create_user(username='follower')

        cls.test_group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание'
        )

        cls.changed_group = Group.objects.create(
            title='Измененная группа',
            slug='changed_group',
            description='Измененное описание'
        )

        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=User.objects.get(username='author'),
            group=Group.objects.get(title='Тестовая группа')
        )

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)

        self.follower_client = Client()
        self.follower_client.force_login(self.follower)

        self.guest = Client()

    def test_post_creating(self):
        post_count = Post.objects.all().count()
        post_data = {'text': 'Пост создан', 'group': self.test_group.id}
        response = self.author_client.post(reverse('posts:create_post'), data=post_data, follow=True)
        profile_data = {'username': self.author.username}

        self.assertEqual(response.status_code, 200)

        self.assertRedirects(response, reverse('posts:profile', kwargs=profile_data))

        self.assertEqual(Post.objects.all().count(), post_count + 1)

        self.assertTrue(Post.objects.filter(text='Пост создан', author=self.author.id).exists())

    def test_post_editing(self):
        post_count = Post.objects.all().count()
        post_data = {'text': 'Пост отредактирован', 'group': self.changed_group.id}
        response = self.author_client.post(reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
                                           data=post_data,
                                           follow=True)
        self.post = Post.objects.all().last()

        self.assertEqual(response.status_code, 200)

        self.assertRedirects(response, reverse('posts:view_post', kwargs={'post_id': self.post.id}))

        self.assertEqual(post_count, Post.objects.count())

        self.assertEqual(self.post.text, 'Пост отредактирован')

        self.assertEqual(self.post.group.title, 'Измененная группа')

        self.assertEqual(self.author, self.post.author)

    def test_following(self):
        self.follower_client.get(reverse('posts:profile_follow', kwargs={'username': self.author.username}),
                                 follow=True)

        is_follow = Follow.objects.filter(author=self.author, user=self.follower).exists()

        self.assertEqual(is_follow, True)

        self.follower_client.get(reverse('posts:profile_unfollow', kwargs={'username': self.author.username}),
                                 follow=True)

        is_follow = Follow.objects.filter(author=self.author, user=self.follower).exists()

        self.assertEqual(is_follow, False)

    def test_comments(self):
        post_data = {'text': 'Тестовый текст'}
        self.guest.post(reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
                        data=post_data,
                        follow=True)
        self.assertEqual(Comment.objects.count(), 0)
        self.author_client.post(reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
                                data=post_data,
                                follow=True)
        self.assertEqual(Comment.objects.count(), 1)
