#include <iostream>
#include <vector>
#include "demo.h"


User *MiddleWare::get_user(const std::string &school, const std::string &city){
    auto *u = new User("zhangsan", 20, 1);
    return u;
}

std::string User::get_name(std::string name){
    return this->name;
};

int User::get_age(int age){
    return this->age;
};

int User::get_id(int id){
    return this->id;
};

int User::get_id1(int id){
    return this->id + 1;
};

int User::get_id2(int id){
    return this->id + 2;
};
