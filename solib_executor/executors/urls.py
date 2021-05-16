from django.urls import path
from executors.executor_view import BaseExecutor
from executors.rule_parse_view import RuleParse
from executors.code_content_view import CodeContent

urlpatterns = [
    path('exec_code', BaseExecutor().as_view()),
    path('parse_rule', RuleParse().as_view()),
    path('code_content', CodeContent().as_view()),
]
