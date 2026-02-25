from django.urls import path

from shared_backend.api import views

create_user_path = path("create-user/", views.CreateUserView.as_view(), name="create-user")
