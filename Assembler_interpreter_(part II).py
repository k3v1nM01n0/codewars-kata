# https://www.codewars.com/kata/58e61f3d8ff24f774400002c/train/python

'''
This is the second part of this kata series. First part is here.

We want to create an interpreter of assembler which will support the following instructions:

mov x, y - copy y (either an integer or the value of a register) into register x.
inc x - increase the content of register x by one.
dec x - decrease the content of register x by one.
add x, y - add the content of the register x with y (either an integer or the value of a register) and stores the result in x (i.e. register[x] += y).
sub x, y - subtract y (either an integer or the value of a register) from the register x and stores the result in x (i.e. register[x] -= y).
mul x, y - same with multiply (i.e. register[x] *= y).
div x, y - same with integer division (i.e. register[x] /= y).
label: - define a label position (label = identifier + ":", an identifier being a string that does not match any other command). Jump commands and call are aimed to these labels positions in the program.
jmp lbl - jumps to the label lbl.
cmp x, y - compares x (either an integer or the value of a register) and y (either an integer or the value of a register). The result is used in the conditional jumps (jne, je, jge, jg, jle and jl)
jne lbl - jump to the label lbl if the values of the previous cmp command were not equal.
je lbl - jump to the label lbl if the values of the previous cmp command were equal.
jge lbl - jump to the label lbl if x was greater or equal than y in the previous cmp command.
jg lbl - jump to the label lbl if x was greater than y in the previous cmp command.
jle lbl - jump to the label lbl if x was less or equal than y in the previous cmp command.
jl lbl - jump to the label lbl if x was less than y in the previous cmp command.
call lbl - call to the subroutine identified by lbl. When a ret is found in a subroutine, the instruction pointer should return to the instruction next to this call command.
ret - when a ret is found in a subroutine, the instruction pointer should return to the instruction that called the current function.
msg 'Register: ', x - this instruction stores the output of the program. It may contain text strings (delimited by single quotes) and registers. The number of arguments isn't limited and will vary, depending on the program.
end - this instruction indicates that the program ends correctly, so the stored output is returned (if the program terminates without this instruction it should return the default output: see below).
; comment - comments should not be taken in consideration during the execution of the program.

Output format:
The normal output format is a string (returned with the end command). For Scala and Rust programming languages it should be incapsulated into Option.

If the program does finish itself without using an end instruction, the default return value is:

-1 (as an integer)

Input format:
The function/method will take as input a multiline string of instructions, delimited with EOL characters. Please, note that the instructions may also have indentation for readability purposes.

For example:

program = """
; My first program
mov  a, 5
inc  a
call function
msg  '(5+1)/2 = ', a    ; output message
end

function:
    div  a, 2
    ret
"""
assembler_interpreter(program)
The above code would set register a to 5, increase its value by 1, calls the subroutine function, divide its value by 2, returns to the first call instruction, prepares the output of the program and then returns it with the end instruction. In this case, the output would be (5+1)/2 = 3.
'''

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