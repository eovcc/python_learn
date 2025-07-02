import multiprocessing
import os, time


def writer(q):
    print(f"writer id:{os.getpid()}, pid:{os.getppid()}")
    for c in "hello":
        q.put(c)


def reader(q):
    print(f"reader id:{os.getpid()}, pid:{os.getppid()}")
    for c in range(q.qsize()):
        print(q.get())


def main():
    q = multiprocessing.Manager().Queue()
    po = multiprocessing.Pool(2)
    po.apply_async(writer, (q,))
    time.sleep(1)
    po.apply_async(reader, (q,))
    po.close()
    po.join()


if __name__ == "__main__":
    main()
