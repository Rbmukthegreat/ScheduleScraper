num = 0

def f(l, n, curr):
    if n == len(l):
        global num
        num += 1
        print(curr)
        return

    prevcurr = curr
    for i in range(len(l)):
        curr += str(i+1)
        f(l, n+1, curr)
        curr = prevcurr


if __name__ == "__main__":
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    f(l, 0, "")
    print(num)
