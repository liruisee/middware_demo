a = {
    "type": "class",
    "is_point": False,
    "point_depth": 0,
    "class_name": "User",
    "key_name": "user",
    "members": [
        {
            "type": "string",
            "is_point": False,
            "point_depth": 0,
            "key_name": "school"
        },
        {
            "type": "string",
            "is_point": False,
            "point_depth": 0,
            "key_name": "city"
        },
        {
            "type": "array",
            "is_point": False,
            "point_depth": 0,
            "key_name": "peoples",
            "sub_desc": {
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
                        "key_name": "name"
                    },
                    {
                        "type": "int",
                        "is_point": False,
                        "point_depth": 0,
                        "key_name": "age"
                    },
                    {
                        "type": "int",
                        "is_point": False,
                        "point_depth": 0,
                        "key_name": "sex"
                    }
                ]
            }
        }
    ]
}


def gen_to_json_methods(return_type):
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


result = gen_to_json_methods(a)
print('\n'.join(result))
