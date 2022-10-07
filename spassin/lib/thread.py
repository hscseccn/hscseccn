from threading import Thread
import threading

lock = threading.Lock()

class MyThread(Thread):#继承Thread类
    def __init__(self, target, args):
        #关于super的用法可以自行百度
        super(MyThread, self).__init__()#初始化Thread
        self.target = target
        self.args = args
    def run(self):
        self.result = self.target(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return e