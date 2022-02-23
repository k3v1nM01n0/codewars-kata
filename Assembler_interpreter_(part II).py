# https://www.codewars.com/kata/58e61f3d8ff24f774400002c/train/python

from re import compile

CMT = compile(r';.*')                # comment
TKN = compile(r"\w+|'.*?'|[^\s,]+")  # tokens

class Interpreter:
    def __init__(self) -> None:
        self.reg = {}  # registry
        self.lbl = {}  # labels
        self.stk = []  # call stack
        self.lns = []  # lines
        self.out = ''  # output
        self.ptr = 0   # line pointer

    @staticmethod
    def tokenize(string: str) -> list:
        return TKN.findall(CMT.sub('', string).strip())

    def get(self, x: str) -> int:
        return self.reg[x] if x in self.reg else int(x)

    def run(self, code: str) -> str or int:
        self.lns = list(filter(None, map(self.tokenize, code.splitlines())))
        while 0 <= self.ptr < len(self.lns):
            cmd, *args = self.lns[self.ptr]
            if cmd == 'end': return self.out
            if hasattr(self, cmd): getattr(self, cmd)(*args)
            self.ptr += 1
        return -1

    def mov(self, x: str, y) -> None:
        self.reg[x] = self.get(y)

    def inc(self, x: str) -> None:
        self.reg[x] += 1

    def dec(self, x: str) -> None:
        self.reg[x] -= 1

    def add(self, x: str, y: str) -> None:
        self.reg[x] += self.get(y)

    def sub(self, x: str, y: str) -> None:
        self.reg[x] -= self.get(y)

    def mul(self, x: str, y: str) -> None:
        self.reg[x] *= self.get(y)

    def div(self, x: str, y: str) -> None:
        self.reg[x] //= self.get(y)

    def jmp(self, label: str) -> None:
        if label in self.lbl:
            self.ptr = self.lbl[label]
            return
        while self.lns[self.ptr][0] != label:
            self.ptr += 1
        self.lbl[label] = self.ptr

    def cmp(self, x: str, y: str) -> None:
        x = self.get(x)
        y = self.get(y)
        self.stk.append((x > y) - (x < y))

    def jne(self, label: str) -> None:
        if self.stk.pop() != 0:  # x != y
            self.jmp(label)

    def je(self, label: str) -> None:
        if self.stk.pop() == 0:  # x == y
            self.jmp(label)

    def jge(self, label: str) -> None:
        if self.stk.pop() >= 0:  # x >= y
            self.jmp(label)

    def jg(self, label: str) -> None:
        if self.stk.pop() > 0:  # x > y
            self.jmp(label)

    def jle(self, label: str) -> None:
        if self.stk.pop() <= 0:  # x <= y
            self.jmp(label)

    def jl(self, label: str) -> None:
        if self.stk.pop() < 0:  # x < y
            self.jmp(label)

    def call(self, label: str) -> None:
        self.stk.append(self.ptr)
        self.jmp(label)

    def ret(self) -> None:
        self.ptr = self.stk.pop()

    def msg(self, *args: str or int) -> None:
        self.out += ''.join(str(self.reg[arg]) if arg in self.reg else arg.strip("'") for arg in args)

def assembler_interpreter(program: str) -> str or int:
    return Interpreter().run(program)