from django.urls import path
from executors.base_executor import BaseExecutor

urlpatterns = [
    path('index', BaseExecutor().as_view()),
]
