"""
struct People{
    std::string name;
    int age;
    int sex;
};

struct User{
    std::string school;
    std::string city;
    std::vector<People> peoples;
};
"""

request_info = {
    "header_file_names": ["demo1.h"],
    "cxx_flags": "-I/usr/local/include",
    "middleware_name": "demo1",
    "class_name": "class1",
    "method_name": "func1",
    "args": [
        {
            "type": "int",
            "is_point": False,
            "point_depth": 0,
            "value": "1",
        },
        {
            "type": "string",
            "is_point": False,
            "point_depth": 0,
            "value": "2"
        },
        {
            "type": "enum",
            "value": "enum_key"
        },
        {
            "type": "class",
            "is_point": False,
            "point_depth": 0,
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


response = {
    "user": {
        "school": "",
        "city": "",
        "peoples": [
            {
                "name": "",
                "age": 0,
                "sex": 0
            },
            {
                "name": "",
                "age": 0,
                "sex": 0
            }
        ],
    }
}