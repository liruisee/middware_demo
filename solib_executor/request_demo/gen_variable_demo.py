import json
import os
import subprocess
import uuid
import datetime
import copy

template_file_path = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/templates/cplus_source_file.cpp.template'
node_map = {item['id']: item for item in a['graph']}


class BaseExecutor:

    def __init__(self):
        self.template_dir = '/Users/lr/PycharmProjects/middware_demo/solib_executor/templates'
        self.var_id = 0
        self.result_id = 0
        self.demo_dir = '/Users/lr/PycharmProjects/middware_demo/demo1'
        self.template_file_path = f'{self.template_dir}/cplus_source_file.cpp.template'
        self.cls_map = {}

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
                if 'rule' in node and node['rule'] != 'placeholder':
                    rules.append((path + ['rule'], node['type'], node['rule']))
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
    def get_to_json_method_codes(return_type_list):
        curr_nodes = return_type_list
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

    def get_node_code(self, node: dict, last_node_var_name: str):
        node_info = node['node_info']
        args = node_info['args']
        node_id = node['id']
        codes = []
        arg_names = []
        for i in range(len(args)):
            arg = args[i]
            if 'rule' in arg and arg['rule'] == 'placeholder':
                arg_name = last_node_var_name
                arg_codes = []
            else:
                arg_name, arg_codes = self.get_variable_codes(arg)
            arg_names.append(arg_name)
            codes.extend(arg_codes)
        arg_str = ', '.join(arg_names)
        method_name = node_info['method_name']
        result_var_name = f'result_{self.result_id}'
        self.result_id += 1

        if 'class_name' in node_info:
            class_name = node_info['class_name']
            method_name = node_info['method_name']
            if class_name == method_name:
                if class_name in self.cls_map:
                    raise Exception(f'class {class_name} can not create again.')

                code = f'{class_name} {result_var_name}({arg_str});'
                self.cls_map[class_name] = result_var_name
            else:

                if class_name not in self.cls_map:
                    raise Exception(f'the class {class_name} has not created.')
                cls_var_name = self.cls_map[class_name]
                code = f'auto {result_var_name} = {cls_var_name}.{method_name}({arg_str});'
            codes.append(code)
        else:
            code = f'auto {result_var_name} = {method_name}({arg_str});'
            codes.append(code)
        result_codes = [
            f'pv = to_json({result_var_name}, d);',
            f'buffer.Clear();',
            f'writer.Reset(buffer);',
            'pv->Accept(writer);',
            f'std::cout << "node_id: {node_id}, execute success, result: " << buffer.GetString() << std::endl;'
        ]
        codes.extend(result_codes)
        return codes, result_var_name

    def get_graph_code(self, curr_node, last_node_var_name=None, level=1, indent=' ' * 4):
        codes = []
        curr_code, result_var_name = self.get_node_code(curr_node, last_node_var_name)
        curr_code_str = indent * level + ('\n' + (indent * level)).join(curr_code)
        codes.append(curr_code_str)
        all_none = all(map(lambda x: x is None, [curr_node['next'], curr_node['next_true'], curr_node['next_false']]))
        if all_none:
            return codes
        if curr_node['next'] is not None and (
                curr_node['next_true'] is not None or curr_node['next_false'] is not None):
            raise Exception(f'node_id: {curr_node["id"]} error, next or true/false')
        if curr_node['next'] is not None:
            codes = codes + self.get_graph_code(node_map[curr_node['next']], result_var_name)
            return codes
        if curr_node['next_true'] is not None:
            codes.append('%sif(true){' % (indent * level))
            codes = codes + self.get_graph_code(node_map[curr_node['next_true']], result_var_name, level + 1)
            codes.append('%s}' % (indent * level))
        if curr_node['next_false'] is not None:
            codes[-1] = codes[-1] + ' else {'
            codes = codes + self.get_graph_code(node_map[curr_node['next_false']], result_var_name, level + 1)
            codes.append('%s}' % (indent * level))
        return codes

    def new_main_code(self, graph):
        codes = [
            'int main(){',
            '    Document d;',
            '    Value *pv = nullptr;',
            '    StringBuffer buffer;',
            '    PrettyWriter <StringBuffer> writer(buffer);',
            '    writer.SetIndent(\' \', 2);'
        ]
        curr_node = graph[0]
        new_codes = self.get_graph_code(curr_node)
        codes.extend(new_codes)
        codes.append('}')
        return codes

    def get_main_code(self, body: dict):
        args = body['args']
        codes_list = []
        rules = self.get_rules(args)
        if len(rules) == 0:
            codes = []
            arg_names = []
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
                'Value *pv = to_json(result, d);',
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
            codes_list.append(codes)
            arg_list = args
        else:
            rule_paths, rule_type, rule_str = rules[0]
            rule_vales = self.rule_to_list(rule_str, rule_type)
            tmp = args
            for k in rule_paths[:-1]:
                tmp = tmp[k]
            del tmp['rule']

            arg_list = []
            for rule_vale in rule_vales:
                codes = []
                arg_names = []
                tmp['value'] = rule_vale
                arg_list.append(copy.deepcopy(args))

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
                    'Value *pv = to_json(result, d);',
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
                codes_list.append(codes)

        return codes_list, arg_list

    def get_render_template_content(self, body: dict):
        header_file_names = body['header_file_names']
        include_codes = self.get_user_include_codes(header_file_names)
        return_type_list = [node['node_info']['return_type'] for node in body['graph']]
        method_code = self.get_to_json_method_codes(return_type_list)
        main_code = self.new_main_code(body['graph'])
        f = open(template_file_path, 'r')
        template_content = f.read()
        f.close()
        results = []

        render_map = {
            'user_include': '\n'.join(include_codes),
            'user_function': '\n'.join(method_code),
            'user_main': '\n'.join(main_code)
        }
        result = template_content % render_map
        return result

    def post(self, body: dict):
        code_contents, arg_list = self.get_render_template_content(body)

        code_results = []
        for i in range(len(code_contents)):
            code_content = code_contents[i]
            arg = arg_list[i]
            time_str = datetime.date.today().strftime('%Y%m%d')
            uid = uuid.uuid1()
            file_id = f'{time_str}-{uid}'
            cpp_file_path = f'{self.template_dir}/{file_id}.cpp'
            target_file_path = f'{self.template_dir}/{file_id}.out'
            with open(cpp_file_path, 'w') as f:
                f.write(code_content)
            build_cmd = \
                f'g++ -std=c++11 {cpp_file_path} -I {self.demo_dir} ' \
                f'-L {self.demo_dir} -ldemo ' \
                f'-o {target_file_path}'
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
                'args': arg,
                'build_result': build_result,
                'exec_result': json.loads(exec_result),
                'exec_code': code_content,
                'file_id': file_id,
                'build_status': build_status,
                'exec_status': exec_status
            }
            code_results.append(tmp)

        return code_results


if __name__ == '__main__':
    data = {
        "header_file_names": ["demo.h"],
        "class_name": "MiddleWare",
        "cxx_flags": "",
        "middleware_name": ["demo"],
        "graph": [
            {
                "id": 1,
                "node_info": {
                    "args": [
                        {
                            "type": "string",
                            "is_point": False,
                            "point_depth": 0,
                            "value": "zhangsan"
                        },
                        {
                            "type": "int",
                            "is_point": False,
                            "point_depth": 0,
                            "value": "50"
                        },
                        {
                            "type": "int",
                            "is_point": False,
                            "point_depth": 0,
                            "value": "3"
                        },
                    ],
                    "class_name": "User",
                    "method_name": "User",
                    "return_type": {
                        "type": "class",
                        "key_name": "user",
                        "class_name": "User",
                        "members": [
                            {
                                "type": "string",
                                "key_name": "name",
                                "is_point": False,
                                "point_depth": 0,
                                "value": "zhangsan"
                            },
                            {
                                "type": "int",
                                "key_name": "age",
                                "is_point": False,
                                "point_depth": 0,
                                "value": "50"
                            },
                            {
                                "type": "int",
                                "key_name": "id",
                                "is_point": False,
                                "point_depth": 0,
                                "value": "3"
                            },
                        ]
                    }
                },
                "next": 2,
                "next_true": None,
                "next_false": None
            },
            {
                "id": 2,
                "node_info": {
                    "args": [
                        {
                            "type": "string",
                            "is_point": False,
                            "point_depth": 0,
                            "value": "zhangsan"
                        }
                    ],
                    "class_name": "User",
                    "method_name": "get_name",
                    "return_type": {
                        "type": "string",
                        "key_name": "name"
                    }
                },
                "next": None,
                "next_true": 3,
                "next_false": 4
            },
            {
                "id": 3,
                "node_info": {
                    "args": [
                        {
                            "type": "int",
                            "is_point": False,
                            "point_depth": 0,
                            "value": "30"
                        }
                    ],
                    "class_name": "User",
                    "method_name": "get_age",
                    "return_type": {
                        "type": "int",
                        "key_name": "age"
                    }
                },
                "next": None,
                "next_true": 5,
                "next_false": 6
            },
            {
                "id": 4,
                "node_info": {
                    "args": [
                        {
                            "type": "int",
                            "is_point": False,
                            "point_depth": 0,
                            "value": "1"
                        }
                    ],
                    "class_name": "User",
                    "method_name": "get_id",
                    "return_type": {
                        "type": "int",
                        "key_name": "id"
                    }
                },
                "next": None,
                "next_true": None,
                "next_false": None
            },
            {
                "id": 5,
                "node_info": {
                    "args": [
                        {
                            "type": "int",
                            "is_point": False,
                            "point_depth": 0,
                            "rule": "placeholder"
                        }
                    ],
                    "class_name": "User",
                    "method_name": "get_id1",
                    "return_type": {
                        "type": "int",
                        "key_name": "id1"
                    }
                },
                "next": None,
                "next_true": None,
                "next_false": None
            },
            {
                "id": 6,
                "node_info": {
                    "args": [
                        {
                            "type": "int",
                            "is_point": False,
                            "point_depth": 0,
                            "rule": "placeholder"
                        }
                    ],
                    "class_name": "User",
                    "method_name": "get_id2",
                    "return_type": {
                        "type": "int",
                        "key_name": "id2"
                    }
                },
                "next": None,
                "next_true": None,
                "next_false": None
            },
        ]

    }

    be = BaseExecutor()
    print(be.get_render_template_content(data))
