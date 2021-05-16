### 本服务提供3个接口，下面分别介绍

#### 一、将包含规则的请求body解析成不含规则的多条body:

##### 请求url
```python
url = "http://api.shhy.tech:10080/middleware/parse_rule"
method = "post"
```

##### 请求body
```python
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
```

##### 返回结果：
```python
response = {
    "result": [
        {
            "header_file_names": [
                "demo1/demo.h"
            ],
            "class_name": "MiddleWare",
            "cxx_flags": "-L /home/nuoer/middware_demo/demo1 -ldemo -I /home/nuoer/middware_demo",
            "middleware_name": [
                "demo"
            ],
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
                            }
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
                                }
                            ]
                        }
                    },
                    "next": 2,
                    "next_true": None,
                    "next_False": None
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
                    "next_False": 4
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
                    "next_False": 6
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
                    "next_False": None
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
                    "next_False": None
                },
                {
                    "id": 6,
                    "node_info": {
                        "args": [
                            {
                                "type": "int",
                                "is_point": False,
                                "point_depth": 0,
                                "value": "0"
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
                    "next_False": None
                }
            ]
        },
        {
            "header_file_names": [
                "demo1/demo.h"
            ],
            "class_name": "MiddleWare",
            "cxx_flags": "-L /home/nuoer/middware_demo/demo1 -ldemo -I /home/nuoer/middware_demo",
            "middleware_name": [
                "demo"
            ],
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
                            }
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
                                }
                            ]
                        }
                    },
                    "next": 2,
                    "next_true": None,
                    "next_False": None
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
                    "next_False": 4
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
                    "next_False": 6
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
                    "next_False": None
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
                    "next_False": None
                },
                {
                    "id": 6,
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
                        "method_name": "get_id2",
                        "return_type": {
                            "type": "int",
                            "is_point": False,
                            "key_name": "id2"
                        }
                    },
                    "next": None,
                    "next_true": None,
                    "next_False": None
                }
            ]
        }
    ],
    "message": "success",
    "status": 200
}
```



=====================================分隔线=====================================
#### 二、将不包含规则或只包含占位符规则的body转换成代码

##### 请求url
```python
url = "http://api.shhy.tech:10080/middleware/code_content"
method = "post"
```

##### 请求body
```python
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
                        "value": "3"
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
                        "value": "1"
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
```

##### 返回结果
```python
response = {
    "result": "#include \"rapidjson/document.h\"\n#include \"rapidjson/writer.h\"\n#include \"rapidjson/stringbuffer.h\"\n#include \"rapidjson/prettywriter.h\"\n#include <iostream>\n#include <vector>\n#include <execinfo.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include \"demo1/demo.h\"\n\nusing namespace rapidjson;\n\n\nValue *to_json(int i, Document &d){\n    auto *pv = new Value();\n    pv->SetInt(i);\n    return pv;\n}\n\nValue *to_json(int* i, Document &d){\n    auto *pv = new Value();\n    if(i == nullptr){\n        pv->SetNull();\n        return pv;\n    }\n    pv->SetInt(*i);\n    return pv;\n}\n\nValue *to_json(std::string &s, Document &d){\n    auto *pv = new Value();\n    pv->SetString(s.c_str(), (int)s.length());\n    return pv;\n}\n\nValue *to_json(std::string* s, Document &d){\n    auto *pv = new Value();\n    if(s == nullptr){\n        pv->SetNull();\n        return pv;\n    }\n    pv->SetString((*s).c_str(), (int)(*s).length());\n    return pv;\n}\n\n\n\nValue *to_json(bool b, Document &d){\n    auto *pv = new Value();\n    pv->SetBool(b);\n    return pv;\n}\n\n\ntemplate<typename T>\nValue *to_json(T *p, Document &d){\n    auto *pv = new Value();\n    if(p == nullptr){\n        pv->SetNull();\n        return pv;\n    }\n    return to_json(*p, d);\n}\n\n\ntemplate<typename T>\nValue *to_json(std::vector<T> &vec, Document &d){\n    auto *pv = new Value();\n    pv->SetArray();\n    for(auto it=begin(vec);it!=end(vec);++it){\n        Value *tmp = to_json(*it, d);\n        pv->PushBack(*tmp, d.GetAllocator());\n    }\n    return pv;\n}\n\ntemplate<typename T>\nValue *to_json(std::vector<T> *vec, Document &d){\n    auto *pv = new Value();\n    if(vec == nullptr){\n        pv->SetNull();\n        return pv;\n    }\n    pv->SetArray();\n    for(auto it=begin(*vec);it!=end(*vec);++it){\n        Value *tmp = to_json(*it, d);\n        pv->PushBack(*tmp, d.GetAllocator());\n    }\n    return pv;\n}\n\nValue *to_json(User &cls, Document &d){\n    auto * pv = new Value();\n    pv->SetObject();\n    pv->AddMember(\"name\", *to_json(cls.name, d), d.GetAllocator());\n    pv->AddMember(\"age\", *to_json(cls.age, d), d.GetAllocator());\n    pv->AddMember(\"id\", *to_json(cls.id, d), d.GetAllocator());\n    return pv;\n}\n\n\n\nint main(){\n    Document d;\n    Value *pv = nullptr;\n    StringBuffer buffer;\n    PrettyWriter <StringBuffer> writer(buffer);\n    writer.SetIndent(' ', 2);\n    std::string var_1 = \"zhangsan\";\n    int var_2 = 50;\n    int var_3 = 3;\n    User result_0(var_1, var_2, var_3);\n    pv = to_json(result_0, d);\n    buffer.Clear();\n    writer.Reset(buffer);\n    pv->Accept(writer);\n    std::cout << \"node_id: 1, execute success, result: \" << buffer.GetString() << std::endl;\n    std::string var_4 = \"zhangsan\";\n    auto result_1 = result_0.get_name(var_4);\n    pv = to_json(result_1, d);\n    buffer.Clear();\n    writer.Reset(buffer);\n    pv->Accept(writer);\n    std::cout << \"node_id: 2, execute success, result: \" << buffer.GetString() << std::endl;\n    if(result_1.empty()){\n        int var_5 = 30;\n        auto result_2 = result_0.get_age(var_5);\n        pv = to_json(result_2, d);\n        buffer.Clear();\n        writer.Reset(buffer);\n        pv->Accept(writer);\n        std::cout << \"node_id: 3, execute success, result: \" << buffer.GetString() << std::endl;\n        if(result_2 == 0){\n            auto result_3 = result_0.get_id1(result_2);\n            pv = to_json(result_3, d);\n            buffer.Clear();\n            writer.Reset(buffer);\n            pv->Accept(writer);\n            std::cout << \"node_id: 5, execute success, result: \" << buffer.GetString() << std::endl;\n        } else {\n            int var_6 = 0;\n            auto result_4 = result_0.get_id2(var_6);\n            pv = to_json(result_4, d);\n            buffer.Clear();\n            writer.Reset(buffer);\n            pv->Accept(writer);\n            std::cout << \"node_id: 6, execute success, result: \" << buffer.GetString() << std::endl;\n        }\n    } else {\n        int var_7 = 1;\n        auto result_5 = result_0.get_id(var_7);\n        pv = to_json(result_5, d);\n        buffer.Clear();\n        writer.Reset(buffer);\n        pv->Accept(writer);\n        std::cout << \"node_id: 4, execute success, result: \" << buffer.GetString() << std::endl;\n    }\n}",
    "message": "success",
    "status": 200
}
```


=====================================分隔线=====================================
#### 三、将不包含规则或只包含占位符规则的body直接执行，生成返回执行结果

##### 请求url
```python
url = "http://api.shhy.tech:10080/middleware/exec_code"
method = "post"
```

##### 请求body
```python
# 同接口2的body
```

##### 返回结果
```python
response = {
    "result": {
        "build_cmd": "g++ -std=c++11 /home/nuoer/middware_demo/solib_executor/templates/20210516-fd5db866-b641-11eb-9304-3448edf736d8.cpp -L /home/nuoer/middware_demo/demo1 -ldemo -I /home/nuoer/middware_demo  -o /home/nuoer/middware_demo/solib_executor/templates/20210516-fd5db866-b641-11eb-9304-3448edf736d8.out",
        "build_result": "",
        "exec_result": "node_id: 1, execute success, result: {\n  \"name\": \"zhangsan\",\n  \"age\": 50,\n  \"id\": 3\n}\nnode_id: 2, execute success, result: \"zhangsan\"\nnode_id: 4, execute success, result: 3",
        "file_id": "20210516-fd5db866-b641-11eb-9304-3448edf736d8",
        "build_status": 0,
        "exec_status": 0
    },
    "message": "success",
    "status": 200
}
```
