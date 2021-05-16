//
// Created by lirui on 2021/4/5.
//

#ifndef HELLOWORLD_DEMO_H
#define HELLOWORLD_DEMO_H

#include <iostream>
#include <vector>


struct User{

public:
    User(std::string name, int age, int id): name(name), age(age), id(id){};
    std::string get_name(std::string name);
    int get_age(int age);
    int get_id(int id);
    int get_id1(int id);
    int get_id2(int id);

    std::string name;
    int age;
    int id;

};

struct MiddleWare{
    User *get_user(const std::string &school, const std::string &city);
};

#endif //HELLOWORLD_DEMO_H
