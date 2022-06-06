

import json
import struct
import random

from z3 import *

from compiler import flatten_ast, ops_to_lines, make_json

ROM_SIZE = 512
STACK_SIZE = 256

def getb(vec, n):
    v = Extract(n,0,vec & ((1 << n) - 1))
    return (vec >> n, v)

def push_stack(stack, val):
    return (stack << 7) + ZeroExt(stack.size() - val.size(), val)

def step():
    rom = BitVec('rom', 8 * ROM_SIZE)
    stack = BitVec('stack', 8 * STACK_SIZE)

    pre = [rom, stack]

    rom, op = getb(rom, 2)

    # hlt : 0
    rom = If(
        op == 0,
        BitVecVal(0, 8 * ROM_SIZE),
        rom
    )

    # push <v> : 1 v
    p_rom, p_val = getb(rom, 7)
    rom = If(op == 1, p_rom, rom)
    stack = If(op == 1, push_stack(stack, p_val), stack)

    # hlt_nz : 2
    cond = Extract(6,0,stack & 0x7f) == 0
    stack = If(
        op == 2,
        If(cond, stack, BitVecVal(0, 8 * STACK_SIZE)),
        stack
    )
    rom = If(
        op == 2,
        If(cond, rom, BitVecVal(0, 8 * ROM_SIZE)),
        rom
    )

    # arith
    arith = {
        0: lambda x, y: x + y, # add
        1: lambda x, y: x - y, # sub
        2: lambda x, y: x * y, # mul
        3: lambda x, y: x ^ y, # xor
    }

    a = Extract(6,0,stack & 0x7f)
    b = Extract(6,0,(stack >> 7) & 0x7f)

    rom_a, k = getb(rom, 2)

    stack = If(
        op == 3,
        If(
            k == 0,
            push_stack(stack >> 14, (arith[0](a,b) & 0x7f)),
            If(
                k == 1,
                push_stack(stack >> 14, (arith[1](a,b) & 0x7f)),
                If(
                    k == 2,
                    push_stack(stack >> 14, (arith[2](a,b) & 0x7f)),
                    push_stack(stack >> 14, (arith[3](a,b) & 0x7f)),
                )
            )
        ),
        stack
    )

    rom = If(
        op == 3,
        rom_a,
        rom
    )

    post = [rom, stack]

    return pre, post


OUTER = {
    "id": "DG4-D",
    "title": "Visual Motion",
    "subtitle": "(for internal use only)",
    "sections": [
        {
            "num": "Part I",
            "title": "General Information",
            "type": "general",
            "fields": [
                {"type": "text", "num": 1, "name": "Field A", "info": "internal use only"}
            ]
        },
        {
            "num": "Part II",
            "title": "Configuration",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "[redacted]",
                    "lines": [] # load ROM
                },
                {
                    "num": "Step 2",
                    "title": "[redacted]",
                    "lines": [] # load stack
                },
                {
                    "num": "Step 3",
                    "title": "[redacted]",
                    "lines": [] # execute
                },
            ]
        },
        {
            "num": "Part III",
            "title": "Result",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "Result",
                    "lines": []
                }
            ]
        }
    ]
}

INNER = {
    "id": "DG7",
    "title": "[redacted]",
    "subtitle": "[redacted]",
    "sections": [
        {
            "num": "Part I",
            "title": "[redacted]",
            "type": "general",
            "fields": [
                {"type": "text", "num": 1, "name": "Field B", "info": "internal use only"}, # rom
                {"type": "text", "num": 2, "name": "Field C", "info": "internal use only"}, # stack
            ]
        },
        {
            "num": "Part II",
            "title": "[redacted]",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "[redacted]",
                    "lines": [] # rom update
                },
                {
                    "num": "Step 2",
                    "title": "[redacted]",
                    "lines": [] # stack update
                }
            ]
        },
        {
            "num": "Part III",
            "title": "[redacted]",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "lmao",
                    "lines": [] # check if rom == 0
                }
            ]
        },
        {
            "num": "Part IV",
            "title": "[redacted]",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "[redacted]",
                    "lines": [] # finalizer
                }
            ]
        }
    ]
}


OPS = [
    lambda x,y: x+y,
    lambda x,y: x-y,
    lambda x,y: x*y,
    lambda x,y: x^y,
]


def gen_rand_expr(n=5):
    if n == 0:
        return BitVecVal(random.randint(0,127), 7)
    
    a = gen_rand_expr(n-1)
    b = gen_rand_expr(n-1)
    
    op = random.choice(OPS)
    
    return op(a,b)


def expr_to_stack(z):
    ops = []
    
    typ = z.decl().name()
    ch = z.children()
    
    ops = {
        'bvsub': 'sub',
        'bvadd': 'add',
        'bvmul': 'mul',
        'bvxor': 'xor'
    }
    
    if typ == 'bv':
        return [f'push {z}']
    elif typ in ops:
        b = expr_to_stack(ch[0])
        a = expr_to_stack(ch[1])
        return b + a + [ops[typ]]
    else:
        print('unkown', typ)
        return []


def gen_stack_assembly(part):
    random.seed(1337)

    ops = []
    for i in range(16):
        z = gen_rand_expr(5)
        val = simplify(z).as_long()

        print('expr: ', z)
        print('simplified: ', val)

        ops += expr_to_stack(z)
        ops += [
            f'push {val ^ part[i]}',
            'xor', # (val ^ expr)
            'xor', # flag ^ (val ^ expr)
            'check',
            'add'
        ]

    ops += [
        'push 1',
        'hlt'
    ]

    return ops


def make_rom(ops):
    rom = 0
    for op in ops[::-1]:
        t = op.split(' ')
        if t[0] == 'hlt':
            rom = (rom << 2) + 0
        elif t[0] == 'push':
            print('push ', t[1])
            rom = (rom << 9) + (int(t[1]) << 2) + 1
        elif t[0] == 'check':
            rom = (rom << 2) + 2
        elif t[0] == 'add':
            rom = (rom << 4) + (0 << 2) + 3
        elif t[0] == 'sub':
            rom = (rom << 4) + (1 << 2) + 3
        elif t[0] == 'mul':
            rom = (rom << 4) + (2 << 2) + 3
        elif t[0] == 'xor':
            rom = (rom << 4) + (3 << 2) + 3
        else:
            print('unknown', t)
    return rom


def load_rom(rom):
    arr = []
    while rom > 0:
        arr.append(rom & 0xffffffff)
        rom >>= 32

    rval = BitVecVal(0, 8 * ROM_SIZE)
    for v in arr[::-1]:
        rval <<= 32
        rval += BitVecVal(v, 8 * ROM_SIZE)

    return rval


def init_stack(flag):
    stack = BitVecVal(0, 8 * STACK_SIZE)
    for i in range(15,-1,-1):
        stack <<= 7
        stack += ZeroExt(stack.size() - flag[i].size(), flag[i])
    return stack


def make4(part):
    pre, post = step()

    custom = {
        pre[0].decl().name(): "Copy the value from line 1.",
        pre[1].decl().name(): "Copy the value from line 2.",
    }

    prev = 2
    out_map = {}
    for i in range(2):
        ops = []
        flatten_ast(post[i], [], ops, custom=custom, protect_size=False, root=prev)
        lines = ops_to_lines(ops)
        INNER['sections'][1]['steps'][i]['lines'] = lines
        prev = lines[-1]['num']
        out_map[i] = prev

    m = prev
    INNER['sections'][2]['steps'][0]['lines'] = [
        {'type': 'op', 'num': m+1, 'msg': f'Copy the value from line {out_map[0]}.'}, # rom
        {'type': 'op', 'num': m+2, 'msg': f'Copy the value from line {out_map[1]}.'}, # stack
        {'type': 'val', 'num': m+3, 'val': '127'},
        {'type': 'op', 'num': m+4, 'msg': f'Perform logical AND between lines {m+2} and {m+3}.'},
        {
            'type': 'choice', 
            'num': m+5, 
            'msg': f'Is line {m+1} equal to 0?', 
            'yes': 'Complete Part IV below.', 
            'no': f'Continue at line {m+6}.'
        },
        {'type': 'op', 'num': m+6, 'msg': f'Complete form "[redacted]" (DG7) using line {m+1} as \"Field A\" and line {m+2} as \"Field B\". Enter the result (DG7, line {m+7}) here.'}
    ]

    inner_form_res_idx = m+7

    INNER['sections'][3]['steps'][0]['lines'] = [
        {'type': 'op', 'num': m+7, 'msg': f'If you answered \"yes\" to line {m+5}, copy the value from line {m+4}. Otherwise, copy the value from line {m+6}.'}
    ]

    ops = gen_stack_assembly(part)
    rom = make_rom(ops)
    print(hex(rom))
    v = load_rom(rom)
    ops = []
    flatten_ast(v, [], ops, protect_size=False, root=1)
    lines = ops_to_lines(ops)
    OUTER['sections'][1]['steps'][0]['lines'] = lines

    rom_val_idx = lines[-1]['num']

    flag = [BitVec('f%d' % i, 8) for i in range(16)]
    stack = init_stack(flag)
    ops = []
    custom = {
        flag[i].decl().name(): f'Copy the ASCII value of the character at index {i} of line 1.'
        for i in range(16)
    }
    flatten_ast(stack, [], ops, custom=custom, root=rom_val_idx, protect_size=False)
    lines = ops_to_lines(ops)

    OUTER['sections'][1]['steps'][1]['lines'] = lines

    stack_val_idx = lines[-1]['num']
    m = stack_val_idx

    OUTER['sections'][1]['steps'][2]['lines'] = [
        {'type': 'op', 'num': m+1, 'msg': f'Copy the value from line {rom_val_idx}.'},
        {'type': 'op', 'num': m+2, 'msg': f'Copy the value from line {stack_val_idx}.'},
        {'type': 'op', 'num': m+3, 'msg': f'Complete form "[redacted]" (DG7) using line {m+1} as \"Field A\" and line {m+2} as \"Field B\". Enter the result (DG7, line {inner_form_res_idx}) here.'}
    ]

    OUTER['sections'][2]['steps'][0]['lines'] = [
        {'type': 'op', 'num': m+4, 'msg': f'Copy the value from line {m+3}.'}
    ]

    open('./builder/forms/DG7.json', 'w').write(json.dumps(INNER))
    open('./builder/forms/DG4-D.json', 'w').write(json.dumps(OUTER))


if __name__=='__main__':
    make4(b'_simul4ti0n_lmao')
