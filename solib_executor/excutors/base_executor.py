from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
import os
import subprocess


template_file_path = os.path.abspath(__file__).rsplit('/', 1)[0] + '/templates/cplus_source_file.cpp.template'


class BaseExecutor(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request: WSGIRequest):
        body = json.loads(request.body.decode('utf-8'))
        lib_name = body['lib_name']
        method_name = body['method_name']
        args = ', '.join(body['args'])
        render_dict = {
            'lib_name': lib_name,
            'method_name': method_name,
            'args': args
        }

        f = open(template_file_path, 'r')
        content = f.read()
        f.close()
        fin_content = content % render_dict
        cpp_file_path = '/tmp/a.cpp'
        target_file_path = '/tmp/a.out'
        with open(cpp_file_path, 'w') as f:
            f.write(fin_content)
        cmd = f'g++ {cpp_file_path} -o  && {target_file_path}'
        result = subprocess.check_output(cmd, shell=True)
        result = {
            'result': result,
            'message': 'success',
            'status': 200
        }
        return JsonResponse(result)
