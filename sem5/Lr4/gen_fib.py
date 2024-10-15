import itertools

def fib(n):
    if n < 0:
        return None
    res_lst = [0, 1]
    while res_lst[-1] + res_lst[-2] <= n:
        res_lst.append(res_lst[-1] + res_lst[-2])
    return res_lst[:n+1]

class FibonacchiLst:
    def __init__(self, max_value):
        self.max_value = max_value
        self.lst = [0, 1]

    def __getitem__(self, idx):
        if self.max_value == 1:
            return self.lst[idx]
        while len(self.lst) <= idx:
            next_fib = self.lst[-1] + self.lst[-2]
            if next_fib > self.max_value:
                raise IndexError(idx)
            self.lst.append(next_fib)
        return self.lst[idx]

def fib_classic_iter():
    a, b = 0, 1
    yield a
    yield b
    while True:
        a, b = b, a + b
        yield b

def fib_iter(num_iterable):
    return itertools.takewhile(lambda x: x <= max(num_iterable), fib_classic_iter())

def main():
    print('fib():')
    print(fib(10))
    print('FibonacchiLst():')
    print(list(FibonacchiLst(10)))
    print('fib_classic_iter():')
    g = fib_classic_iter()
    for _ in range(15):
        print(next(g), end=' ')
    print()

    print('fib_iter(range(10))')
    for el in fib_iter(range(15)):
        print(el, end=' ')

if __name__ == '__main__':
    main()


