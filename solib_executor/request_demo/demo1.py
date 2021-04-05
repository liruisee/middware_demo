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
                "type": "enum",
                "is_point": False,
                "point_depth": 0,
                "key_name": "city",
                "value": "enum_key"
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
}

res = requests.post(url, json=data)
print(res.json()['result']['exec_result'])
