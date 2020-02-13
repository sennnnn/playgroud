#include <stdlib.h>
#include <time.h>

#include "curses.h"
#include "world.h"
#include "variable.h"

void init()
{
    int x,y;
    // printf("1");
    initscr();      // 初始化，进入 ncurses 模式。
    cbreak();       // cbreak() or raw() 虽然我不知道二者有什么区别，不过这两个函数的主要作用就是将字符输入不需要回车什么的。
    noecho();       // 是否将输入的字符输出到 stdscr 上。
    curs_set(0);    // 用来设置光标是否可见，0 (不可见)，1 (可见)，2 (完全可见)。

    empty = 15;
    srand(time(0));
    x = rand() % 4;
    y = rand() % 4;
    a[x][y] = 2;
    draw();
}

void draw()
{
    int n,m,x,y;
    char c[4] = {'0','0','0','0'};
    clear();

    // 绘制横线
    for(n = 0; n < 9; n += 2)
    {
        // 总共有四行格子，所以应该有五行横线，而为了留一行空行用来绘制数字。
        for(m = 0; m < 21; m++)
        {
            // 有 4 列格子，每个格子留 4 个单元，那么就应该有 21 列，
            move(n, m);
            addch('-');
            refresh();
        }
    }

    // 绘制竖线
    for(n = 1; n < 9; n += 2)
    {
        for(m = 0; m < 21; m += 5)
        {
            move(n, m);
            addch('|');
            refresh();
        }
    }

    // 绘制数字
    for(int x = 0; x < 4; x++)
    {
        for(int y = 0; y < 4; y++)
        {
            draw_number(x, y);
        }
    }
}

void draw_number(int x, int y)
{
    int i,m,k,j;
    // 所有元素默认被初始化为 0x00。
    char c[5] = {0x00};
    i = a[x][y];
    m = 0;
    while(i != 0)
    {
        j = i % 10;
        c[m++] = j + '0';
        i = i / 10;
    }
    m = 0;
    k = 5*(y+1)-1;
    while(c[m] != 0x00)
    {
        move(2*x+1, k);
        addch(c[m++]);
        refresh();
        k--;        
    }
}

void play()
{
    int x,y,i,new_x,new_y,temp;
    int old_empty,move = 0;
    char ch;

    while(1)
    {
        move = 0;
        old_empty = empty;
        ch = getch();
        switch(ch)
        {
        case 'a':   // 字母 'a'
        case 68:    // 左移方向键
            for(x = 0; x < 4; x++)
                {
                    for(y = 0; y < 4; y++)
                    {
                        if(a[x][y] == 0)
                        {
                            // 扫描这一行
                            y++;
                            continue;
                        }
                        else
                        {
                            for(i = y + 1; i < 4; i++)
                            {
                                if(a[x][i] == 0)
                                {
                                    continue;
                                }
                                else
                                {
                                    if(a[x][y] == a[x][i])
                                    {
                                        a[x][y] += a[x][i];
                                        a[x][i] = 0;
                                        empty++;
                                        break;
                                    }
                                }
                            }
                        }
                        
                    }
                    for(y = 0; y < 4; y++)
                    {
                        if(a[x][y] == 0)
                        {
                            continue;
                        }
                        else
                        {
                            for(i = y - 1; i > 0; i--)
                            {
                                if(a[x][i] == 0)
                                {
                                    a[x][i] = a[x][i+1];
                                    a[x][i+1] = 0;
                                    move = 1;
                                }
                                else
                                {
                                    break;
                                }
                            }
                        }
                    }
                }
            break;
        case 'd':   // 字母 d
        case 67:    // 右移方向键
            for(x = 0; x < 4; x++)
                {
                    for(y = 4; y > 0; y--)
                    {
                        if(a[x][y] == 0)
                        {
                            // 扫描这一行
                            y--;
                            continue;
                        }
                        else
                        {
                            for(i = y - 1; i > 0; i--)
                            {
                                if(a[x][i] == 0)
                                {
                                    continue;
                                }
                                else
                                {
                                    if(a[x][y] == a[x][i])
                                    {
                                        a[x][y] += a[x][i];
                                        a[x][i] = 0;
                                        empty++;
                                        break;
                                    }
                                }
                            }
                        }
                        
                    }
                    for(y = 0; y < 4; y++)
                    {
                        if(a[x][y] == 0)
                        {
                            continue;
                        }
                        else
                        {
                            for(i = y + 1; i < 4; i++)
                            {
                                if(a[x][i] == 0)
                                {
                                    a[x][i] = a[x][i-1];
                                    a[x][i-1] = 0;
                                    move = 1;
                                }
                                else
                                {
                                    break;
                                }
                            }
                        }
                    }
                }
            break;
        case 'w' :  // 字母 w
        case 65 :   // 上移方向键
            for(y = 0; y < 4; y++)
                {
                    for(x = 0; x < 4; x++)
                    {
                        if(a[x][y] == 0)
                        {
                            // 扫描这一行
                            y--;
                            continue;
                        }
                        else
                        {
                            for(i = x + 1; i < 4; i++)
                            {
                                if(a[i][y] == 0)
                                {
                                    continue;
                                }
                                else
                                {
                                    if(a[x][y] == a[i][y])
                                    {
                                        a[x][y] += a[i][y];
                                        a[i][y] = 0;
                                        empty++;
                                        break;
                                    }
                                }
                            }
                        }
                        
                    }
                    for(x = 4; x > 0; x--)
                    {
                        if(a[x][y] == 0)
                        {
                            continue;
                        }
                        else
                        {
                            for(i = x - 1; i > 0; i--)
                            {
                                if(a[i][y] == 0)
                                {
                                    a[i][y] = a[i+1][y];
                                    a[i+1][y] = 0;
                                    move = 1;
                                }
                                else
                                {
                                    break;
                                }
                            }
                        }
                    }
                }
        case 's' :  // 字母 s
        case 66 :   // 下移方向键
            for(y = 0; y < 4; y++)
                {
                    for(x = 4; x > 0; x--)
                    {
                        if(a[x][y] == 0)
                        {
                            // 扫描这一行
                            x--;
                            continue;
                        }
                        else
                        {
                            for(i = x - 1; i > 0; i--)
                            {
                                if(a[i][y] == 0)
                                {
                                    continue;
                                }
                                else
                                {
                                    if(a[x][y] == a[i][y])
                                    {
                                        a[x][y] += a[i][y];
                                        a[i][y] = 0;
                                        empty++;
                                        break;
                                    }
                                }
                            }
                        }
                        
                    }
                    for(x = 0; x < 4; x++)
                    {
                        if(a[x][y] == 0)
                        {
                            continue;
                        }
                        else
                        {
                            for(i = x + 1; i < 4; i++)
                            {
                                if(a[i][y] == 0)
                                {
                                    a[i][y] = a[i-1][y];
                                    a[i-1][y] = 0;
                                    move = 1;
                                }
                                else
                                {
                                    break;
                                }
                            }
                        }
                    }
                }
        case 'Q' : 
        case 'q' :
            game_over();
            break;
        default:
            continue;
            break;
        }
        if(empty <= 0)
            game_over;
        if(empty != old_empty || move == 1)
        {
            do
            {
                new_x = rand()%4;
                new_y = rand()%4;
            }
            while(a[new_x][new_y] != 0);
            
            // cnt_value(&new_x, &new_y);

            do
            {
                temp = rand()%4;
            }while(temp == 1 || temp == 3);
            a[new_x][new_y] = temp;
            empty--;
            
            draw();
        }
    }
}

int game_over()
{
    sleep(1);
    endwin();
    exit(0);
}