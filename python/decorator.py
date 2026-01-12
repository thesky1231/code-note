# 当想要给很多个函数加同样的功能的时候可以用修饰器做到
def decorator_func(old_func):
    def new_func():
        # 加入功能
        old_func()
    return new_func


# 下面写一个给函数添加运行时间计算的修饰器
import time
def add_time(old_func):
    def new_func():
        Start = time.time()
        old_func()
        End = time.time()
        print(f"运行时间为{End - Start}")