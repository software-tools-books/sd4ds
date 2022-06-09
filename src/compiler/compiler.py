"""Turn text into code."""

import sys

from architecture import NUM_REG, OP_INSTR, OP_SHIFT, RAM_LEN

DIVIDER = ".data"


class Assembler:
    def __init__(self):
        pass

    def assemble(self, lines):
        lines = self.cleanLines(lines)
        labels = self.findLabels(lines)
        instructions, allocations = self.split(lines)
        instructions = [ln for ln in instructions if not self.isLabel(ln)]
        baseOfData = len(instructions)
        self.addAllocations(baseOfData, labels, allocations)
        compiled = [self.compile(instr, labels) for instr in instructions]
        program = self.instructionsToText(compiled)
        return program

    def cleanLines(self, lines):
        lines = [ln.strip() for ln in lines]
        lines = [ln for ln in lines if len(ln) > 0]
        lines = [ln for ln in lines if not self.isComment(ln)]
        return lines

    def split(self, lines):
        try:
            i = lines.index(DIVIDER)
            return lines[:i], lines[i + 1 :]
        except ValueError:
            return lines, []

    def isComment(self, line):
        return line[0] == "#"

    def findLabels(self, lines):
        result = {}
        index = 0
        for ln in lines:
            if self.isLabel(ln):
                label = ln.rstrip(":")
                assert label not in result, f"Duplicate label {label}"
                result[label] = index
            else:
                index += 1
        return result

    def isLabel(self, line):
        return line[-1] == ":"

    def compile(self, instruction, labels):
        fields = instruction.split()
        op, args = fields[0], fields[1:]
        assert op in OP_INSTR, f"Unknown operation {op}"
        op = OP_INSTR[op]

        if op.fmt == "--":
            return self.combine(op.code)
        if op.fmt == "r-":
            return self.combine(self.reg(args[0]), op.code)
        if op.fmt == "rr":
            return self.combine(self.reg(args[1]), self.reg(args[0]), op.code)
        if op.fmt == "rv":
            return self.combine(self.value(args[1], labels), self.reg(args[0]), op.code)

        assert False, f"Unknown instruction format {op.fmt}"

    def combine(self, *args):
        assert len(args) > 0, "Cannot combine no arguments"
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        return result

    def addAllocations(self, baseOfData, labels, toAllocate):
        for alloc in toAllocate:
            fields = [f.strip() for f in alloc.split(":")]
            assert len(fields) == 2, f"Invalid allocation directive '{alloc}'"
            label, numWords = fields
            assert label not in labels, f"Duplicate label '{label}' in data allocation"
            numWords = int(numWords)
            assert (
                baseOfData + numWords
            ) < RAM_LEN, f"Allocation '{label}' requires too much memory"
            labels[label] = baseOfData
            baseOfData += numWords

    def instructionsToText(self, program):
        return [f"{op:06x}" for op in program]

    def reg(self, token):
        assert token[0] == "R", f"Register '{token}' does not start with 'R'"
        r = int(token[1:])
        assert (0 <= r) and (r < NUM_REG), f"Illegal register {token}"
        return r

    def value(self, token, labels):
        if token[0] != "@":
            return int(token)
        labelName = token[1:]
        assert labelName in labels, f"Unknown label '{token}'"
        return labels[labelName]


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    a = Assembler()
    for code in a.assemble(lines):
        print(code)
