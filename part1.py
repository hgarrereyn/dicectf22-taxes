
import json

from compiler import flatten_ast, build_checker, ops_to_lines, make_json

def fn1(flag):
    k1 = b'DiceGangDanceGig'
    enc = [flag[i] ^ k1[i] for i in range(16)]
    return enc


def make1(part):
    v, flag = build_checker(part, fn1)

    ops = []
    flatten_ast(v, flag, ops, root=1)

    lines = ops_to_lines(ops)
    j = make_json('DG4-A', 'Xenial Obsidian Router', '(for internal use only)', lines)
    open('./builder/forms/DG4-A.json', 'w').write(json.dumps(j))


if __name__=='__main__':
    make1(b'int3rn4l_r3venue')
