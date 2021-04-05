from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
import os
import subprocess
from base_app.exceptions import ViewException
import re
import random


template_file_path = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates/cplus_source_file.cpp.template'


class BaseExecutor(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_dir = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates'
        self.demo_dir = str(os.path.abspath(__file__).rsplit('/', 3)[0]) + '/demo1'
        self.var_id = 0

    @staticmethod
    def get_user_include_codes(header_file_names: list):
        codes = []
        for header_file in header_file_names:
            code = f'#include "{header_file}"'
            codes.append(code)
        return codes

    @staticmethod
    def get_rules(args):
        rules = []
        curr_nodes = []
        for i in range(len(args)):
            arg = args[i]
            curr_nodes.append(([i], arg))
        while len(curr_nodes) > 0:
            tmp = []
            for path, node in curr_nodes:
                if 'rule' in node:
                    rules.append((path + ['rule'], node['rule']))
                elif node['type'] in ('int', 'string', 'bool'):
                    continue
                elif node['type'] == 'enum':
                    continue
                elif node['type'] == 'class':
                    mems = node['members']
                    for i in range(len(mems)):
                        mem = mems[i]
                        tmp.append((path + ['members', i], mem))
                elif node['type'] == 'array':
                    mems = node['members']
                    for i in range(len(mems)):
                        mem = mems[i]
                        tmp.append((path + ['members', i], mem))
                else:
                    raise Exception(f'the type {node["type"]} not support')
            curr_nodes = tmp
        if len(rules) >= 2:
            rule_paths = [' -> '.join(map(repr, rule[0])) for rule in rules]
            raise Exception(f'the rule count can not more than one, but found: {rule_paths}')
        return rules

    @staticmethod
    def rule_to_list(rule_str):
        regexp = re.compile('rand\( *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            result = [round(random.random(), 4)]
            return result

        regexp = re.compile('rand\( *(\d+) *, *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = int(match.group(1))
            end = int(match.group(2))
            result = [round(random.random(), 4) * (end - start) + start]
            return result

        regexp = re.compile('randint\( *(\d+) *, *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = int(match.group(1))
            end = int(match.group(2))
            result = [random.randint(start, end)]
            return result

        regexp = re.compile('periphery\( *(\d+(?:\.\d+)?) *, *(\d+(?:\.\d+)?) *, *(\d+(?:\.\d+)?) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = float(match.group(1))
            end = float(match.group(2))
            precision = float(match.group(3))
            result = [
                round(start - precision, 6),
                round(start + precision, 6),
                round(end - precision, 6),
                round(end + precision, 6)
            ]
            return result

        regexp = re.compile('range\( *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = 0
            end = int(match.group(1))
            step = 1
            result = []
            while start < end:
                result.append(start)
                start += step
            return result

        regexp = re.compile('range\( *(\d+) *, *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = int(match.group(1))
            end = int(match.group(2))
            step = 1
            result = []
            while start < end:
                result.append(start)
                start += step
            return result

        regexp = re.compile('range\( *(\d+) *, *(\d+) *, *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = int(match.group(1))
            end = int(match.group(2))
            step = int(match.group(3))
            result = []
            if step == 0:
                raise Exception('step can not be 0.')
            if step < 0:
                while start > end:
                    result.append(start)
                    start += step
            else:
                while start < end:
                    result.append(start)
                    start += step
            return result

    def get_variable_codes(self, arg_json: dict):
        self.var_id += 1
        var_id = self.var_id
        curr_node = arg_json
        type_map = {
            'int': 'int',
            'string': 'std::string',
            'bool': 'bool'
        }
        if curr_node['type'] in ('int', 'string', 'bool'):
            _type_str = type_map[curr_node['type']]
            val = curr_node['value']
            var_name = f'var_{var_id}'
            codes = []
            if curr_node['type'] == 'string':
                code = f'{_type_str} {var_name} = "{val}";'
            else:
                code = f'{_type_str} {var_name} = {val};'
            codes.append(code)

            if curr_node['is_point'] is True:
                for i in range(curr_node['point_depth']):
                    if i == 0:
                        tmp_var_name = f'p_{var_name}'
                        code = f'{_type_str} *{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    else:
                        tmp_var_name = f'p{var_name}'
                        code = f'{_type_str} {"*" * (i+1)}{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    codes.append(code)
            return var_name, codes

        if curr_node['type'] == 'enum':
            _type_str = curr_node['enum_name']
            var_name = f'var_{var_id}'
            val = curr_node['value']
            codes = []
            code = f'{_type_str} {var_name} = {val};'
            codes.append(code)

            if curr_node['is_point'] is True:
                for i in range(curr_node['point_depth']):
                    if i == 0:
                        tmp_var_name = f'p_{var_name}'
                        code = f'{_type_str} *{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    else:
                        tmp_var_name = f'p{var_name}'
                        code = f'{_type_str} {"*" * (i+1)}{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    codes.append(code)
            return var_name, codes

        if curr_node['type'] == 'class':
            var_name = f'var_{var_id}'
            class_name = curr_node['class_name']
            codes = []
            code = f'{class_name} {var_name};'
            codes.append(code)
            mems = curr_node['members']
            for i in range(len(mems)):
                mem = mems[i]
                mem_var_name, mem_var_codes = self.get_variable_codes(mem)
                codes.extend(mem_var_codes)
                mem_name = mem['key_name']
                tmp_code = f'{var_name}.{mem_name} = {mem_var_name};'
                codes.append(tmp_code)

            if curr_node['is_point'] is True:
                for i in range(curr_node['point_depth']):
                    if i == 0:
                        tmp_var_name = f'p_{var_name}'
                        code = f'{class_name} *{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    else:
                        tmp_var_name = f'p{var_name}'
                        code = f'{class_name} {"*" * (i+1)}{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    codes.append(code)

            return var_name, codes

        if curr_node['type'] == 'array':
            var_name = f'var_{var_id}'
            mems = curr_node['members']
            sub_type_set = {mem['type'] for mem in mems}
            if len(sub_type_set) != 1:
                raise Exception(f'the array mem type must be unique, but found {sub_type_set}')
            sub_type = sub_type_set.pop()
            if sub_type == 'class':
                sub_class_set = {mem['class_name'] for mem in mems}
                if len(sub_class_set) != 1:
                    raise Exception(f'the array mem class type must be unique, but found {sub_class_set}')
                sub_class_name = sub_class_set.pop()
                type_str = f'std::vector<{sub_class_name}>'
            else:
                type_str = f'std::vector<{sub_type}>'
            codes = []
            code = f'{type_str} {var_name};'
            codes.append(code)

            for i in range(len(mems)):
                mem = mems[i]
                mem_var_name, mem_var_codes = self.get_variable_codes(mem)
                codes.extend(mem_var_codes)
                tmp_code = f'{var_name}.push_back({mem_var_name});'
                codes.append(tmp_code)

            if curr_node['is_point'] is True:
                for i in range(curr_node['point_depth']):
                    if i == 0:
                        tmp_var_name = f'p_{var_name}'
                        code = f'{type_str} *{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    else:
                        tmp_var_name = f'p{var_name}'
                        code = f'{type_str} {"*" * (i+1)}{tmp_var_name} = &{var_name};'
                        var_name = tmp_var_name
                    codes.append(code)
            return var_name, codes

    @staticmethod
    def get_to_json_method_codes(return_type):
        curr_nodes = [return_type]
        codes = []
        class_set = set()
        while len(curr_nodes) > 0:
            curr_node = curr_nodes.pop()
            if curr_node['type'] in ('int', 'string', 'bool'):
                continue
            if curr_node['type'] == 'array':
                curr_nodes.append(curr_node['sub_desc'])
                continue
            if curr_node['type'] == 'class':
                class_name = curr_node['class_name']
                if class_name in class_set:
                    continue
                class_set.add(class_name)
                code = f'Value *to_json({class_name} &cls, Document &d){{'
                codes.append(code)
                code = '    auto * pv = new Value();'
                codes.append(code)
                code = '    pv->SetObject();'
                codes.append(code)
                mems = curr_node['members']
                for mem in mems:
                    mem_name = mem['key_name']
                    code = f'    pv->AddMember("{mem_name}", *to_json(cls.{mem_name}, d), d.GetAllocator());'
                    codes.append(code)
                    curr_nodes.append(mem)
                code = '    return pv;'
                codes.append(code)
                code = '}\n\n'
                codes.append(code)
        return codes

    def get_main_code(self, body: dict):
        args = body['args']
        arg_names = []
        codes = []
        for i in range(len(args)):
            arg = args[i]
            arg_name, arg_codes = self.get_variable_codes(arg)
            arg_names.append(arg_name)
            codes.extend(arg_codes)
        arg_str = ', '.join(arg_names)
        method_name = body['method_name']
        if 'class_name' in body:
            class_name = body['class_name']
            code = f'{class_name} cls;'
            codes.append(code)
            code = f'auto result = cls.{method_name}({arg_str});'
            codes.append(code)
        else:
            code = f'auto result = {method_name}({arg_str});'
            codes.append(code)
        result_codes = [
            'Document d;',
            'Value *pv = to_json(pppp_var_1, d);',
            'StringBuffer buffer;',
            'PrettyWriter <StringBuffer> writer(buffer);',
            'writer.SetIndent(\' \', 2);',
            'pv->Accept(writer);',
            'std::cout << buffer.GetString() << std::endl;'
        ]
        codes.extend(result_codes)
        codes = [f'    {code}' for code in codes]
        codes.insert(0, 'int main(){')
        codes.append('}')
        return codes

    def get_render_template_content(self, body: dict):
        header_file_names = body['header_file_names']
        include_codes = self.get_user_include_codes(header_file_names)
        return_type = body['return_type']
        method_code = self.get_to_json_method_codes(return_type)
        main_code = self.get_main_code(body)
        render_map = {
            'user_include': '\n'.join(include_codes),
            'user_function': '\n'.join(method_code),
            'user_main': '\n'.join(main_code)
        }
        f = open(template_file_path, 'r')
        result = f.read() % render_map
        return result

    def post(self, request: WSGIRequest):
        body = json.loads(request.body.decode('utf-8'))
        code_content = self.get_render_template_content(body)
        cpp_file_path = f'{self.template_dir}/a.cpp'
        target_file_path = f'{self.template_dir}/a.out'
        with open(cpp_file_path, 'w') as f:
            f.write(code_content)
        build_cmd = \
            f'g++ {cpp_file_path} -I {self.demo_dir} ' \
            f'-L {self.demo_dir} -ldemo1 ' \
            f'-o {target_file_path}'
        build_status, build_result = subprocess.getstatusoutput(build_cmd)
        status = 200
        if build_status != 0:
            exec_result = 'build failed, can not execute'
            status = 500
        else:
            exec_cmd = \
                f'export DYLD_LIBRARY_PATH={self.demo_dir} &&' \
                f'export LD_LIBRARY_PATH={self.demo_dir} &&' \
                f'{target_file_path}'
            exec_status, exec_result = subprocess.getstatusoutput(exec_cmd)
            if exec_status != 0:
                status = 500

        result = {
            'result': {
                'build_result': build_result,
                'exec_result': exec_result
            },
            'message': 'success',
            'status': status
        }
        return JsonResponse(result)
