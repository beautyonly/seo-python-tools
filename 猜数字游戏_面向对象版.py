import random

class game(object):
    def __init__(self,name='猜数字游戏',bot=1,top=100,times=5):
        self.__name = name
        self.__top = top
        self.__bot = bot
        self.__times = times
    
    def ResetAns(self,bot,top):
        self.__bot = bot
        self.__top = top
        self.__answer = random.randint(bot+1,top-1)
    
    def ResetTimes(self,times):
        self.__times = times

    def Default(self):
        self.__init__()
    
    def Play(self):
        bot = self.__bot
        top = self.__top
        times = self.__times
        self.ResetAns(bot,top)
        print(self.__answer)
        while True:
            try:
                num = int(input('输入一个%s~%s之间的整数\n' %(bot,top)))
                assert bot < num < top
            except:
                print('不要输入奇怪的东西')
            else:
                times = times - 1
                if num == self.__answer:
                    print('bingo')
                    break
                elif times == 0:
                    print('机会用尽还是没猜对，游戏结束\n正确答案是%s' %self.__answer)
                    break
                elif num > self.__answer:
                    top = num
                elif num < self.__answer:
                    bot = num