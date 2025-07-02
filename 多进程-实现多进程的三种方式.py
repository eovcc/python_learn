import multiprocessing


# 只能是全局函数，不能是嵌套函数
def work1(times):
    for i in range(times):
        print("work1 is working...")


# 方式1
def method1():
    p = multiprocessing.Process(target=work1, args=(5,))
    p.start()


class work2(multiprocessing.Process):
    def __init__(self, times):
        super().__init__()
        self.times = times

    def run(self):
        for i in range(self.times):
            print("work2 is working")


# 方法2
def method2():
    p = work2(5)
    p.start()


# 方法3
def work3(times):
    for i in range(times):
        print("work3 is working...")


def method3():
    po = multiprocessing.Pool(1)
    po.apply_async(work3, (3,))
    po.close()  # 不在往池中添加任务
    po.join()  # 合并进程流，主进程阻塞，否则主进程直接结束


def main():
    # method1()
    # method2()
    method3()


if __name__ == "__main__":
    main()
