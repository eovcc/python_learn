import functools

def main():
    def add(a, b, c, d):
        return a+b+c+d
    

    def partial(func, /, *args, **keywords):
        def wrapper(*wrapper_args, **wrapper_keywords):
            # 合并关键字参数（新参数优先）
            merged_keywords = {**keywords, **wrapper_keywords}
            # 合并位置参数（预绑定参数 + 新参数）
            return func(*args, *wrapper_args, **merged_keywords)
        return wrapper
    p_add = functools.partial(add, 1)
    print(p_add(1, 2, 3, ))
    # n_add = partial(add, a=1)
    # n_add(1, 2, 3, a=4)


if __name__ == "__main__":
    main()