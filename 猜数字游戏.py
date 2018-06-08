#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
top = 100
bottom = 1
ans = random.randint(bottom,top)
times = 5
print('猜数字游戏')

temp = input('\n输入一个整数：')
while temp.isdigit() == False or (int(temp) > 100 or int(temp) < 1):
    while temp.isdigit() == False:
        temp = input('数据类型错误，重新输入')
    while int(temp) > 100 or int(temp) < 1:
        temp = input('超出范围，请输入1~100的数字')
num = int(temp)

while num != ans and times > 1:
    if num > ans:
        top = num
        print('\n错，答案介于%s ~ %s之间' %(bottom,top))
    else:
        bottom = num
        print('\n错，答案介于%s ~ %s之间' %(bottom,top))
    temp = input('还有%d次机会,请继续猜：' %(times -1))
    while temp.isdigit() == False or (int(temp) > 100 or int(temp) < 1):
        while temp.isdigit() == False:
            temp = input('数据类型错误，重新输入')
        while int(temp) > 100 or int(temp) < 1:
            temp = input('超出范围，请输入1~100的数字')
    num = int(temp)
    times = times - 1
if times < 1:
    print('Bingo! 游戏结束，答案是%s' %ans)
else:
    print('\n5次机会用尽还是没猜对，游戏结束\n\n答案是%s' %ans)
