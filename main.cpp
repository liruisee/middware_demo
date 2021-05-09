#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/prettywriter.h"
#include <iostream>
#include <vector>
#include <execinfo.h>
#include <stdio.h>
#include <stdlib.h>
#include "demo1/demo.h"

using namespace rapidjson;


Value *to_json(int i, Document &d){
    auto *pv = new Value();
    pv->SetInt(i);
    return pv;
}

Value *to_json(int* i, Document &d){
    auto *pv = new Value();
    if(i == nullptr){
        pv->SetNull();
        return pv;
    }
    pv->SetInt(*i);
    return pv;
}

Value *to_json(std::string &s, Document &d){
    auto *pv = new Value();
    pv->SetString(s.c_str(), (int)s.length());
    return pv;
}

Value *to_json(std::string* s, Document &d){
    auto *pv = new Value();
    if(s == nullptr){
        pv->SetNull();
        return pv;
    }
    pv->SetString((*s).c_str(), (int)(*s).length());
    return pv;
}



Value *to_json(bool b, Document &d){
    auto *pv = new Value();
    pv->SetBool(b);
    return pv;
}


template<typename T>
Value *to_json(T *p, Document &d){
    auto *pv = new Value();
    if(p == nullptr){
        pv->SetNull();
        return pv;
    }
    return to_json(*p, d);
}


template<typename T>
Value *to_json(std::vector<T> &vec, Document &d){
    auto *pv = new Value();
    pv->SetArray();
    for(auto it=begin(vec);it!=end(vec);++it){
        Value *tmp = to_json(*it, d);
        pv->PushBack(*tmp, d.GetAllocator());
    }
    return pv;
}

template<typename T>
Value *to_json(std::vector<T> *vec, Document &d){
    auto *pv = new Value();
    if(vec == nullptr){
        pv->SetNull();
        return pv;
    }
    pv->SetArray();
    for(auto it=begin(*vec);it!=end(*vec);++it){
        Value *tmp = to_json(*it, d);
        pv->PushBack(*tmp, d.GetAllocator());
    }
    return pv;
}

Value *to_json(User &cls, Document &d){
    auto * pv = new Value();
    pv->SetObject();
    pv->AddMember("school", *to_json(cls.school, d), d.GetAllocator());
    pv->AddMember("city", *to_json(cls.city, d), d.GetAllocator());
    pv->AddMember("peoples", *to_json(cls.peoples, d), d.GetAllocator());
    return pv;
}


Value *to_json(People &cls, Document &d){
    auto * pv = new Value();
    pv->SetObject();
    pv->AddMember("name", *to_json(cls.name, d), d.GetAllocator());
    pv->AddMember("p_name", *to_json(cls.p_name, d), d.GetAllocator());
    pv->AddMember("age", *to_json(cls.age, d), d.GetAllocator());
    pv->AddMember("p_age", *to_json(cls.p_age, d), d.GetAllocator());
    pv->AddMember("sex", *to_json(cls.sex, d), d.GetAllocator());
    return pv;
}



int main(){
    std::string var_1 = "1";
    std::string var_2 = "beijing";
    MiddleWare cls;
    auto result = cls.get_user(var_1, var_2);
    Document d;
    Value *pv = to_json(result, d);
    StringBuffer buffer;
    PrettyWriter <StringBuffer> writer(buffer);
    writer.SetIndent(' ', 2);
    pv->Accept(writer);
    std::cout << buffer.GetString() << std::endl;
}
