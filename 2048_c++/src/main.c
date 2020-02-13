// 尖括号的 include 会直接只在系统文件中寻找，而带引号的 include 会先在用户目录下寻找，然后再到 c++ 安装目录，最后在系统文件中查找。
#include <stdio.h>
#include <stdlib.h>

#include "curses.h"
#include "world.h"
#include "variable.h"

int main(int argv, char ** argc)
{
    init();
    play();
    endwin(); // 退出 ncurses 模式
    getchar();
}