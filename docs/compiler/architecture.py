"""Architecture definitions."""

from pydantic import BaseModel


class Op(BaseModel):
    instr: str
    code: int
    fmt: str
    info: str


OPS = [
    Op(instr="hlt", code=1, fmt="--", info="Halt program"),
    Op(instr="ldc", code=2, fmt="rv", info="Load immediate"),
    Op(instr="ldr", code=3, fmt="rr", info="Load register"),
    Op(instr="cpy", code=4, fmt="rr", info="Copy register"),
    Op(instr="str", code=5, fmt="rr", info="Store register"),
    Op(instr="add", code=6, fmt="rr", info="Add"),
    Op(instr="sub", code=7, fmt="rr", info="Subtract"),
    Op(instr="beq", code=8, fmt="rv", info="Branch if equal"),
    Op(instr="bne", code=9, fmt="rv", info="Branch if not equal"),
    Op(instr="prr", code=10, fmt="r-", info="Print register"),
    Op(instr="prm", code=11, fmt="r-", info="Print memory"),
]
OP_CODES = {op.code: op for op in OPS}
OP_INSTR = {op.instr: op for op in OPS}

OP_MASK = 0xFF  # select a single byte
OP_SHIFT = 8  # shift up by one byte

NUM_REG = 4  # number of registers
RAM_LEN = 256  # number of words in RAM
