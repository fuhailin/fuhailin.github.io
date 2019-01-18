#include <stdio.h> // 请用gcc和g++分别进行编译
int main()
{
    foo(); // foo()在它的声明/定义之前被调用
}

int foo()
{
    printf("Hello");
    return 0;
}
