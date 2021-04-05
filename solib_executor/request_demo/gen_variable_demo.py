a = {
            "type": "class",
            "is_point": True,
            "point_depth": 4,
            "class_name": "User",
            "members": [
                {
                    "type": "string",
                    "is_point": False,
                    "point_depth": 0,
                    "key_name": "school",
                    "value": "6"
                },
                {
                    "type": "string",
                    "is_point": False,
                    "point_depth": 0,
                    "key_name": "city",
                    "value": "7"
                },
                {
                    "type": "array",
                    "is_point": False,
                    "point_depth": 0,
                    "key_name": "peoples",
                    "members": [
                        {
                            "type": "class",
                            "is_point": False,
                            "point_depth": 0,
                            "class_name": "People",
                            "key_name": "people",
                            "members": [
                                {
                                    "type": "string",
                                    "is_point": False,
                                    "point_depth": 0,
                                    "key_name": "name",
                                    "value": "8"
                                },
                                {
                                    "type": "int",
                                    "is_point": False,
                                    "point_depth": 0,
                                    "key_name": "age",
                                    "value": "9"
                                },
                                {
                                    "type": "int",
                                    "is_point": False,
                                    "point_depth": 0,
                                    "key_name": "sex",
                                    "value": "10"
                                }
                            ]
                        },
                        {
                            "type": "class",
                            "is_point": False,
                            "point_depth": 0,
                            "class_name": "People",
                            "key_name": "people",
                            "members": [
                                {
                                    "type": "string",
                                    "is_point": False,
                                    "point_depth": 0,
                                    "key_name": "name",
                                    "value": "11"
                                },
                                {
                                    "type": "int",
                                    "is_point": False,
                                    "point_depth": 0,
                                    "key_name": "age",
                                    "value": "12"
                                },
                                {
                                    "type": "int",
                                    "is_point": False,
                                    "point_depth": 0,
                                    "key_name": "sex",
                                    "value": "13"
                                }
                            ]
                        },

                    ]
                },
            ]
        }


var_id = 0


def gen_variable(arg_json: dict):
    global var_id
    var_id += 1
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

    if curr_node['type'] == 'class':
        var_name = f'var_{var_id}'
        class_name = curr_node['class_name']
        codes = []
        code = f'{class_name} {var_name};'
        codes.append(code)
        mems = curr_node['members']
        for i in range(len(mems)):
            mem = mems[i]
            mem_var_name, mem_var_codes = gen_variable(mem)
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
            type_str = f'vector<{sub_class_name}>'
        else:
            type_str = f'vector<{sub_type}>'
        codes = []
        code = f'{type_str} {var_name};'
        codes.append(code)

        for i in range(len(mems)):
            mem = mems[i]
            mem_var_name, mem_var_codes = gen_variable(mem)
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


result = gen_variable(a)
print(result[0], '\n' + '\n'.join(result[1]))
