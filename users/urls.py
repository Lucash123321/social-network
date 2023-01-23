from django.urls import path
from . import views

urlpatterns = [
        path("singup/", views.SignUp.as_view(), name="signup")
        ]

