from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
import os
import subprocess
from base_app.exceptions import ViewException


template_file_path = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates/cplus_source_file.cpp.template'


class BaseExecutor(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_dir = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates'
        self.demo_dir = str(os.path.abspath(__file__).rsplit('/', 3)[0]) + '/demo1'

    def post(self, request: WSGIRequest):
        body = json.loads(request.body.decode('utf-8'))
        header_file_name = body['header_file_name']
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

        args_define = ';\n    '.join(arg_define_list)
        arg_str = ', '.join(arg_list)
        return_type = body['return_type']
        if return_type == 'void':
            exec_code_list = [
                args_define,
                f'{method_name}({arg_str})',
                f'cout << "\\x01" << "None" << "\\x01" << endl;'
            ]
        elif return_type == 'string':
            exec_code_list = [
                args_define,
                f'{return_type} result = {method_name}({arg_str})',
                f'cout << "\\x01\\x22" <<  << result << "\\x22\\x01" << endl;'
            ]
        elif return_type in num_type_set:
            exec_code_list = [
                args_define,
                f'{return_type} result = {method_name}({arg_str})',
                f'cout << "\\x01" << result << "\\x01" << endl;'
            ]
        else:
            raise ViewException(f'not support return type: {return_type}')

        exec_code = ';\n    '.join(exec_code_list)

        render_dict = {
            'header_file_name': header_file_name,
            'method_name': method_name,
            'exec_code': exec_code
        }

        f = open(template_file_path, 'r')
        content = f.read()
        f.close()
        fina_content = content % render_dict
        cpp_file_path = f'{self.template_dir}/a.cpp'
        target_file_path = f'{self.template_dir}/a.out'
        with open(cpp_file_path, 'w') as f:
            f.write(fina_content)
        cmd = f'g++ {cpp_file_path} -I {self.demo_dir} ' \
              f'-L {self.demo_dir} -ldemo1 ' \
              f'-o {target_file_path} ' \
              f'&& export DYLD_LIBRARY_PATH={self.demo_dir}' \
              f'&& export LD_LIBRARY_PATH={self.demo_dir}' \
              f' && {target_file_path}'
        result = subprocess.check_output(cmd, shell=True)
        result = {
            'result': result.decode('utf-8'),
            'message': 'success',
            'status': 200
        }
        return JsonResponse(result)
