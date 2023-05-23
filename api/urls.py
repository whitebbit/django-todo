from django.urls import path
from .views import GetTask, PostTask, PutTask, DeleteTask

urlpatterns = [
    path("<int:pk>", PutTask.as_view()),
    path("", GetTask.as_view()),
    path("create", PostTask.as_view()),
    path("delete/<int:pk>", DeleteTask.as_view()),
]
