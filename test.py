import functools
import time

# def main():
#     def add(a, b, c, d):
#         return a+b+c+d
    

#     def partial(func, /, *args, **keywords):
#         def wrapper(*wrapper_args, **wrapper_keywords):
#             # 合并关键字参数（新参数优先）
#             merged_keywords = {**keywords, **wrapper_keywords}
#             # 合并位置参数（预绑定参数 + 新参数）
#             return func(*args, *wrapper_args, **merged_keywords)
#         return wrapper
#     p_add = functools.partial(add, 1)
#     print(p_add(1, 2, 3, ))
#     # n_add = partial(add, a=1)
#     # n_add(1, 2, 3, a=4)


def main():
    def count_time(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            rst = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func}函数耗时{(end-start)*1000:.3f}ms")
            return rst
        return wrapper
    
    def trys(times):
        def mid(func):
            def wrapper(*args, **kwargs):
                for i in range(times):
                    print(f"第{i+1}次尝试...")
                    try:
                        rst = func(*args, **kwargs)
                        break
                    except:
                        pass
                return rst
            return wrapper
        return mid

    def partial(*args, **kwargs):
        def mid(func):
            def wrapper(*wargs, **wkwargs):
                merged_kwargs = {**kwargs, **wkwargs}
                rst = func(*args, *wargs, **merged_kwargs)
                return rst
            return wrapper
        return mid


    @trys(3)
    @count_time
    @partial(30000000)
    def func(n):
        for i in range(n):
            pass

    func()


if __name__ == "__main__":
    main()