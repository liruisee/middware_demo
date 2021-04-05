import requests
import json
import re


url = 'http://api.shhy.tech:10080/executors/index'
data = {
    'header_file_names': ['demo.h'],
    'class_name': 'MiddleWare',
    'method_name': 'get_user',
    'args': [
        {
            'type': 'string',
            'value': 'zhangsan',
            "is_point": False,
            "point_depth": 0
        },
        {
            'type': 'string',
            'value': 'beijing',
            "is_point": False,
            "point_depth": 0
        }
    ],
    'return_type': {
        "type": "class",
        "class_name": "User",
        "key_name": "user",
        "members": [
            {
                "type": "string",
                "key_name": "school"
            },
            {
                "type": "string",
                "key_name": "city"
            },
            {
                "type": "enum",
                "key_name": "city",
                "value": "enum_key"
            },
            {
                "type": "array",
                "key_name": "peoples",
                "sub_desc": {
                    "type": "class",
                    "class_name": "People",
                    "key_name": "people",
                    "members": [
                        {
                            "type": "string",
                            "key_name": "name"
                        },
                        {
                            "type": "string",
                            "key_name": "p_name"
                        },
                        {
                            "type": "int",
                            "key_name": "age"
                        },
                        {
                            "type": "int",
                            "key_name": "p_age"
                        },
                        {
                            "type": "int",
                            "key_name": "sex"
                        }
                    ]
                }
            }
        ]
    }
}

res = requests.post(url, json=data)
print(res.json()['result']['exec_result'])
print(res.json())
