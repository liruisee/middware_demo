from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
import os
import subprocess
import uuid
import datetime
from executors.gen_code_util import GenCode


class BaseExecutor(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_dir = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates'
        self.demo_dir = str(os.path.abspath(__file__).rsplit('/', 3)[0]) + '/demo1'
        self.var_id = 0

    def post(self, request: WSGIRequest):
        body = json.loads(request.body.decode('utf-8'))
        gen_code = GenCode(body)
        code_content = gen_code.get_render_template_content()
        cxx_flags = body['cxx_flags']

        time_str = datetime.date.today().strftime('%Y%m%d')
        uid = uuid.uuid1()
        file_id = f'{time_str}-{uid}'
        cpp_file_path = f'{self.template_dir}/{file_id}.cpp'
        target_file_path = f'{self.template_dir}/{file_id}.out'
        with open(cpp_file_path, 'w') as f:
            f.write(code_content)
        build_cmd = \
            f'g++ -std=c++11 {cpp_file_path} ' \
            f'{cxx_flags} ' \
            f' -o {target_file_path}'
        build_status, build_result = subprocess.getstatusoutput(build_cmd)
        if build_status != 0:
            exec_result = 'build failed, can not execute'
            exec_status = -1
        else:
            exec_cmd = \
                f'export DYLD_LIBRARY_PATH={self.demo_dir} &&' \
                f'export LD_LIBRARY_PATH={self.demo_dir} &&' \
                f'{target_file_path}'
            exec_status, exec_result = subprocess.getstatusoutput(exec_cmd)

        tmp = {
            'build_cmd': build_cmd,
            'build_result': build_result,
            'exec_result': exec_result,
            # 'exec_code': code_content,
            'file_id': file_id,
            'build_status': build_status,
            'exec_status': exec_status
        }

        result = {
            'result': tmp,
            'message': 'success',
            'status': 200
        }
        return JsonResponse(result)
