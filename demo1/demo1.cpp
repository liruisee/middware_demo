#include "demo1.h"


void print_args(){
    std::cout << std::endl;
}

template <typename Arg, typename... T>
 void print_args(Arg arg, T... t){
    int argsLength = sizeof...(t);
    if(argsLength == 0){
        std::cout << arg;
    }else{
        std::cout << arg << ", ";
    }
    print_args(t...);
}

void func1(){
    std::cout << "func1 call" << std::endl;
}

void func2(int a, int b, int c){
    std::cout << "func2传入的参数为：";
    print_args(a, b, c);
    std::cout << "func2 call" << std::endl;
}

int func3(int a, std::string b, char c){
    std::cout << "func3传入的参数为：";
    print_args(a, b, c);
    std::cout << "func3 call" << std::endl;
    return 1;
}
