from django.test import Client, TestCase
from posts.models import Group, User, Post
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile


class PostViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test_group',
        )
        cls.author = User.objects.create_user(
            username='author'
        )

        cls.follower = User.objects.create_user(
            username='follower'
        )

        cls.user = User.objects.create_user(
            username='user'
        )

        for number in range(1, 10):
            cls.post = Post.objects.create(
                group=Group.objects.get(slug='test_group'),
                author=User.objects.get(username='author'),
                text=f'Тестовый текст {number}'
            )

        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        cls.uploaded = SimpleUploadedFile('image.gif', cls.image)

        cls.post = Post.objects.create(
            group=Group.objects.get(slug='test_group'),
            text='random_text',
            author=User.objects.get(username='author'),
            image=cls.uploaded)

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)

        self.follower_client = Client()
        self.follower_client.force_login(self.follower)

        self.user_client = Client()
        self.user_client.force_login(self.user)

    def test_views(self):
        template_used = {
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}): 'posts/group_posts.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}): 'posts/create_post.html',
            reverse('posts:create_post'): 'posts/create_post.html',
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:profile', kwargs={'username': self.author.username}): 'posts/profile.html',
            reverse('posts:view_post', kwargs={'post_id': self.post.id}): 'posts/view_post.html'
            }

        for view, template in template_used.items():
            with self.subTest(True):
                response = self.author_client.get(view)
                self.assertTemplateUsed(response, template)

    def test_index_context(self):
        response = self.author_client.get(reverse('posts:index'))
        context = response.context.get('page_obj').object_list
        posts = list(Post.objects.all())[:10]
        self.assertEqual(posts, context)

    def test_profile_context(self):
        response = self.author_client.get(reverse('posts:profile', kwargs={'username': self.author.username}))
        context = response.context.get('page_obj').object_list
        posts = list(Post.objects.all())[:10]
        self.assertEqual(posts, context)

    def test_group_posts_context(self):
        response = self.author_client.get(reverse('posts:group_posts', kwargs={'slug': self.group.slug}))
        context = response.context.get('page_obj').object_list
        posts = list(Post.objects.all())[:10]
        self.assertEqual(posts, context)

    def test_view_post_context(self):
        response = self.author_client.get(reverse('posts:view_post', kwargs={'post_id': 5}))
        context_post = response.context.get('post')
        context_count = response.context.get('posts_count')
        database_count = Post.objects.filter(author=self.author.id).count()
        database_post = Post.objects.get(id=5)
        self.assertEqual(database_count, context_count)
        self.assertEqual(context_post, database_post)

    def test_create_post_context(self):
        response = self.author_client.get(reverse('posts:create_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
            }
        for requested, expected in form_fields.items():
            with self.subTest(True):
                got = response.context['form'].fields[requested]
                self.assertIsInstance(got, expected)

    def test_post_edit_context(self):
        response = self.author_client.get(reverse('posts:post_edit', kwargs={'post_id': 5}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
            }
        for requested, expected in form_fields.items():
            with self.subTest(True):
                got = response.context['form'].fields[requested]
                self.assertIsInstance(got, expected)

    def test_post_on_pages(self):

        form_fields = {
            reverse('posts:index'): Post.objects.get(id=10),
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}): Post.objects.get(id=10),
            reverse('posts:profile', kwargs={'username': self.author.username}): Post.objects.get(id=10)
        }

        for request, expected in form_fields.items():
            response = self.author_client.get(request)
            posts = response.context.get('page_obj').object_list
            self.assertIn(expected, posts)

    def test_image_on_pages(self):

        pages_includes_image = {
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.author.username}),
            }

        for request in pages_includes_image:
            with self.subTest(True):
                response = self.author_client.get(request)
                context = response.context['page_obj'][0]
                self.assertEqual(context.image, self.post.image)

    def test_image_in_post(self):
        response = self.author_client.get(reverse('posts:view_post', kwargs={'post_id': self.post.id}))
        context = response.context['post']
        self.assertEqual(context.image, self.post.image)

    def test_follow_page(self):

        self.follower_client.get(reverse('posts:profile_follow', kwargs={'username': self.author}), follow=True)
        author_posts = list(Post.objects.filter(author__following__user=self.follower))
        response = self.follower_client.get(reverse('posts:follow_index'))
        context = response.context.get('page_obj').object_list
        self.assertEqual(context, author_posts)

        response = self.user_client.get(reverse('posts:follow_index'))
        context = list(response.context.get('page_obj'))
        self.assertEqual(context, [])


class PaginatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            slug='test_group',
            title='Тестовая группа',
        )
        for number in range(1, 21):
            cls.post = Post.objects.create(
                author=User.objects.get(username='author'),
                group=Group.objects.get(slug='test_group'),
                text=f'Тестовый текст {number}'
            )

    def setUp(self):
        self.user = Client()
        self.user.force_login(user=self.author)

    def test_first_page(self):
        form_fields = (
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.author.username})
        )
        expected = list(Post.objects.all()[:10])
        for request in form_fields:
            response = self.user.get(request)
            posts = response.context.get('page_obj').object_list
            self.assertEqual(expected, posts)

    def test_second_page(self):
        form_fields = (
            reverse('posts:index') + '?page=2',
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}) + '?page=2',
            reverse('posts:profile', kwargs={'username': self.author.username}) + '?page=2'
        )
        expected = list(Post.objects.all()[10:20])
        for request in form_fields:
            response = self.user.get(request)
            posts = response.context.get('page_obj').object_list
            self.assertEqual(expected, posts)
