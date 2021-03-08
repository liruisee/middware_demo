from rest_framework.views import APIView
from base_app.base_logger import get_logger
from base_app.exceptions import ViewException
from django.core.handlers.wsgi import WSGIRequest


class BaseViewMeta(type):

    def __new__(mcs, name: str, bases: tuple, attr_map: dict):
        return super().__new__(mcs, name, bases, attr_map)

    def __init__(cls, name: str, bases: tuple, attr_map: dict):
        super().__init__(name, bases, attr_map)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class BaseView(APIView, metaclass=BaseViewMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app_name = self.__class__.__module__.split('.', 1)[0]
        self.logger = get_logger(app_name=app_name, level='DEBUG')

    def get(self, request: WSGIRequest, *args, **kwargs):
        url = request.get_raw_uri()
        raise ViewException(f'path: {url} not support get method')

    def post(self, request: WSGIRequest, *args, **kwargs):
        url = request.get_raw_uri()
        raise ViewException(f'path: {url} not support post method')

    def put(self, request: WSGIRequest, *args, **kwargs):
        url = request.get_raw_uri()
        raise ViewException(f'path: {url} not support put method')

    def delete(self, request: WSGIRequest, *args, **kwargs):
        url = request.get_raw_uri()
        raise ViewException(f'path: {url} not support delete method')
