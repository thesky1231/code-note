# 当想要给很多个函数加同样的功能的时候可以用修饰器做到
def decorator_func(old_func):
    def new_func():
        # 加入功能
        old_func()
    return new_func
# 手动修饰：
def func():
    pass
func = decorator_func(func)


# 下面写一个给函数添加运行时间计算的修饰器
# 无参数修饰器写法
import time
def add_time(old_func):
    def new_func():
        Start = time.time()
        old_func()
        End = time.time()
        print(f"运行时间为{End - Start}")


# 带参数修饰器写法
# 修饰器本身只能传入函数指针这一个参数，哪怕后面位置还有参数，实际上也并没有传入 
# fail: decorator_func(old_func, *args) 这里第二个参数不会传入
def decorator_func(old_func):
    # *args打包所有位置参数 **kwargs打包所有关键字参数
    def new_func(*args, **kwargs):
        # 新加逻辑
        return old_func(*args, **kwargs)
    return new_func


# 那要是修饰器本身也要传入参数呢？
# 再嵌套一层函数，这层函数会返回一个新的修饰器
def add_times(times: int):
    def decorator_func(old_func):
        def new_func(*args, **kwargs):
            for i in range(times):
                print(f"注意！")
            return old_func(*args, **kwargs)
        return new_func
    return decorator_func
        