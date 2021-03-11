from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
import os
import subprocess
from base_app.exceptions import ViewException


template_file_path = str(os.path.abspath(__file__).rsplit('/', 1)[0]) + '/templates/cplus_source_file.cpp.template'


class BaseExecutor(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request: WSGIRequest):
        body = json.loads(request.body.decode('utf-8'))
        lib_name = body['lib_name']
        method_name = body['method_name']
        args = body['args']
        num_type_set = {
            'int', 'float', 'double', 'long', 'long long', 'unsigned', 'unsigned long', 'unsigned long long'
        }
        other_type_set = {
            'string'
        }
        all_type_set = num_type_set | other_type_set
        arg_define_list = []
        arg_list = []
        i = 0
        for arg in args:
            arg_name = f'arg{i}'
            arg_list.append(arg_name)
            _type = arg['type']
            value = arg['value']
            if _type in num_type_set:
                i += 1
                tmp = f'{_type} {arg_name} = {value}'
                arg_define_list.append(tmp)
            elif _type == 'string':
                tmp = f'{_type} {arg_name} = "{value}"'
                arg_define_list.append(tmp)
            else:
                raise ViewException(f'the {arg_name} type: {_type} not in {all_type_set}')

        args_define = ';\n'.join(arg_define_list)
        arg_str = ', '.join(arg_list)

        render_dict = {
            'lib_name': lib_name,
            'method_name': method_name,
            'args_define': args_define,
            'args': arg_str
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
