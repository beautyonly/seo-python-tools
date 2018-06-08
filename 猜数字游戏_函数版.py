import random
def numgame(bot=1,top=100,times=5):
    ans = random.randint(bot,top)
    while True:
        try:
            num = int(input('输入一个%s~%s之间的整数\n' %(bot,top)))
            assert bot < num < top
        except:
            print('不要输入奇怪的东西')
        else:
            times = times - 1
            if times == 0 and num != ans:
                print('机会用尽还是没猜对，游戏结束\n正确答案是%s' %ans)
                break
            elif num == ans:
                print('bingo')
                break
            elif num > ans:
                top = num
            elif num < ans:
                bot = num

numgame()