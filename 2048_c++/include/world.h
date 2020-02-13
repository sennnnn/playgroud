#ifndef WORLD_H
#define WORLD_H

void draw();  // 用于绘制游戏界面
void play();  // 游戏运行的逻辑主体
void init();  // 初始化函数，用于完成一些必要的初始化操作
void draw_number(int , int );  // 绘制单个数字
void cnt_value(int *, int *);  
int game_over();  // 结束游戏
int cnt_one(int , int );  
#endif