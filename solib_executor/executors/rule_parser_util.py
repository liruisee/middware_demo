import json
import re
import random
import copy


class RuleParser:

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
    def get_rules(body: dict):
        rules = []
        curr_nodes = []
        graph = body['graph']
        for i in range(len(graph)):
            args = graph[i]['node_info']['args']
            for j in range(len(args)):
                arg = args[j]
                curr_nodes.append((['graph', i, 'node_info', 'args', j], arg))
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

        mutil_rules = []
        for rule in rules:
            if 'range' in rules[0][2] or 'periphery' in rule[2]:
                mutil_rules.append(rule)

        if len(mutil_rules) > 1:
            err_msgs = ['the graph contains more than one mutil_rule: ']
            for mutil_rule in mutil_rules:
                path_str = ' -> '.join(map(repr, mutil_rule))
                err_msgs.append(path_str)
            err_msg_str = '\n'.join(err_msgs)
            raise Exception(err_msg_str)

        elif len(mutil_rules) == 1:
            rule_path = mutil_rules[0][0]
            rule_node = body[rule_path[0]][rule_path[1]]
            path_str = ' -> '.join(map(repr, rule_path))
            all_none = all([rule_node['next'] is None, rule_node['next_true'] is None, rule_node['next_false'] is None])
            if not all_none:
                if 'range' in rules[0][2] or 'periphery' in rules[0][2]:
                    raise Exception(
                        f'the node: {rule_node["id"]} is not the final node, can not contains range or periphery rule. rule path: {path_str}')

        return rules

    @staticmethod
    def rule_to_list(rule_str, rule_type):
        regexp = re.compile('rand\( *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            result = [round(random.random(), 4)]
            if rule_type != 'int':
                raise Exception(f'rand rule only support int type')
            return result

        regexp = re.compile('rand\( *(\d+) *, *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = int(match.group(1))
            end = int(match.group(2))
            result = [round(random.random(), 4) * (end - start) + start]
            if rule_type != 'int':
                raise Exception(f'rand rule only support int type')
            return result

        regexp = re.compile('randint\( *(\d+) *, *(\d+) *\)$')
        match = re.match(regexp, rule_str)
        if match is not None:
            start = int(match.group(1))
            end = int(match.group(2))
            result = [random.randint(start, end)]
            if rule_type != 'int':
                raise Exception(f'randint rule only support int type')
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
            if rule_type != 'float':
                raise Exception(f'periphery rule only support float type')
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
            # if rule_type != 'int':
            #     raise Exception(f'range rule only support int type')
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
            # if rule_type != 'int':
            #     raise Exception(f'range rule only support int type')
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
            if rule_type != 'int':
                raise Exception(f'range rule only support int type')
            return result
        raise Exception(f'not support rule: {rule_str}')

    def render_rule_to_body(self, body: dict):
        result = []
        rules = self.get_rules(body)
        mutil_rule_index = None
        for i in range(len(rules)):
            rule = rules[i]
            if 'range' in rule[2] or 'periphery' in rule[2]:
                mutil_rule_index = i
                break
        if mutil_rule_index not in (None, 0):
            rules[0], rules[mutil_rule_index] = rules[mutil_rule_index], rules[0]

        vals = self.rule_to_list(rules[0][2], rules[0][1])
        for val in vals:
            new_body = copy.deepcopy(body)
            curr_path = new_body
            for path in rules[0][0][:-1]:
                curr_path = curr_path[path]
            del curr_path['rule']
            curr_path['value'] = str(val)
            for oth_rule in rules[1:]:
                oth_val = self.rule_to_list(oth_rule[2], oth_rule[1])[0]
                curr_path = new_body
                for path in rules[0][0][:-1]:
                    curr_path = curr_path[path]
                del curr_path['rule']
                curr_path['value'] = str(oth_val)
            result.append(new_body)
        return result


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
                            "value": "3",
                            # "rule": "range(10)"
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
                            "rule": "range(2)"
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

    be = RuleParser()
    print(json.dumps(be.render_rule_to_body(data), indent=2, ensure_ascii=False))
