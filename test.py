class A:
    def __init__(self, a):
        self.a = a

D = {1: 2, 4: 20}
apple = A(D)

D[1] = 100
print(apple.a[1])