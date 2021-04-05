from django.urls import path
from excutors.base_executor import BaseExecutor

urlpatterns = [
    path('index', BaseExecutor().as_view()),
]
