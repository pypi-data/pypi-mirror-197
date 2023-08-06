class Calc:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def add(self):
        return self.a + self.b
    
    def sub(self):
        return self.a - self.b
    
    def mul(self):
        return self.a * self.b
    
    def div(self):
        return self.a / self.b

def SayHello():
    print("sup world from srcmake")
    
if __name__ == '__main__':
    SayHello()

