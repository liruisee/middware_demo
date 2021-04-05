//
// Created by lirui on 2021/4/5.
//

#ifndef HELLOWORLD_DEMO_H
#define HELLOWORLD_DEMO_H

#include <iostream>
#include <vector>

struct People{
    std::string name;
    std::string *p_name = nullptr;
    int age;
    int *p_age = nullptr;
    int sex;
    int *p_sex;
};

struct User{
    std::string school;
    std::string city;
    std::vector<People > peoples;
};

struct MiddleWare{
    User *get_user(const std::string &school, const std::string &city);
};

#endif //HELLOWORLD_DEMO_H
