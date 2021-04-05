#include <iostream>
#include <vector>
#include "demo.h"


User *MiddleWare::get_user(const std::string &school, const std::string &city){
    auto *u = new User();
    u->school = school;
    u->city = city;
    u->peoples = std::vector<People>();
    People *peo = new People();
    peo->name = "zhangsan";
    peo->p_name = &peo->name;
    peo->age = 20;
    peo->p_age = &peo->age;
    peo->sex = 1;
    peo->p_sex = &peo->sex;
    u->peoples.push_back(*peo);

    peo = new People();
    peo->name = "lisi";
    peo->p_name = &peo->name;
    peo->age = 25;
    peo->p_age = &peo->age;
    peo->sex = 0;
    peo->p_sex = &peo->sex;
    u->peoples.push_back(*peo);
    return u;
}

