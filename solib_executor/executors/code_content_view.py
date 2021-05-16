from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
import os
from executors.gen_code_util import GenCode


class CodeContent(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_dir = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates'
        self.demo_dir = str(os.path.abspath(__file__).rsplit('/', 3)[0]) + '/demo1'
        self.var_id = 0

    def post(self, request: WSGIRequest):
        body = json.loads(request.body.decode('utf-8'))
        gen_code = GenCode(body)
        code_content = gen_code.get_render_template_content()

        result = {
            'result': code_content,
            'message': 'success',
            'status': 200
        }
        return JsonResponse(result)
