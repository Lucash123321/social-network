from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path("author/", views.about_author, name='author'),
    path("tech/", views.technologies, name='tech')
    ]