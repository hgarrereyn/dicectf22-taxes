
import json
import struct

from z3 import *

from compiler import flatten_ast, build_checker, ops_to_lines, make_json


SEED = 0


def rand():
    global SEED
    SEED = ((SEED * 1103515245) + 12345) & 0x7fffffff
    return SEED


def fn2(flag):
    global SEED
    SEED = BitVecVal(struct.unpack('<I', b'DICE')[0], 32)

    flag = [ZeroExt(24, x) for x in flag]

    for i in range(5):
        for j in range(16):
            flag[j] *= rand()

    return flag


def make2(part):
    v, flag = build_checker(part, fn2)

    ops = []
    flatten_ast(v, flag, ops, root=1)

    lines = ops_to_lines(ops)
    j = make_json('DG4-B', 'Petal Robot Nemo Gladiator', '(for internal use only)', lines)
    open('./builder/forms/DG4-B.json', 'w').write(json.dumps(j))


if __name__=='__main__':
    make2(b'_serv1ce_m0re_l1')
