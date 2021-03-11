//
// Created by lirui on 2021/3/7.
//

#ifndef MIDDWARE_DEMO_DEMO1_H
#define MIDDWARE_DEMO_DEMO1_H

#include <iostream>

extern "C" void func1();

extern "C" void func2(int, int, int);

extern "C" int func3(int, std::string &&, char);

#endif //MIDDWARE_DEMO_DEMO1_H
