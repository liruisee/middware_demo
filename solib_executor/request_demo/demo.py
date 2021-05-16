import requests
import json


# url = 'http://localhost:8080/middleware/parse_rule'
url = 'http://api.shhy.tech:10080/middleware/parse_rule'
body = {
    "header_file_names": ["demo1/demo.h"],
    "class_name": "MiddleWare",
    "cxx_flags": "-L /home/nuoer/middware_demo/demo1 -ldemo -I /home/nuoer/middware_demo",
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
                    "is_point": False,
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
                    "is_point": False,
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
                    "is_point": False,
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
                    "is_point": False,
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
                    "is_point": False,
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
                    "is_point": False,
                    "key_name": "id2"
                }
            },
            "next": None,
            "next_true": None,
            "next_false": None
        },
    ]
}

response = requests.post(url, json=body)
result = response.json()

# print(json.dumps(result, indent=4, ensure_ascii=False))
new_body = result['result'][0]
# url = 'http://localhost:8080/middleware/exec_code'
url = 'http://api.shhy.tech:10080/middleware/exec_code'

response = requests.post(url, json=new_body)
result = response.json()
print(json.dumps(result, indent=4, ensure_ascii=False))
