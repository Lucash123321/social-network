from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'


class Post(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(Group, blank=True, null=True,
                              on_delete=models.SET_NULL, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

