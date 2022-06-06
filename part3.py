
import json
import struct

from z3 import *

from compiler import flatten_ast, ops_to_lines, make_json


def rule_30_step():
    z = BitVec('state', 128)

    bits = []
    for i in range(128):
        bits.append((z >> i) & 1)

    out = [0] * 128

    for i in range(128):
        n_idx = [(i-1) % 128, i, (i + 1) % 128]

        vals = [bits[k] for k in n_idx]
        
        out[i] = If(
            vals[0] == 1,
            If(
                vals[1] == 1,
                BitVecVal(0, 1),
                If(
                    vals[2] == 1,
                    BitVecVal(0, 1),
                    BitVecVal(1, 1),
                )
            ),
            If(
                vals[1] == 1,
                BitVecVal(1, 1),
                If(
                    vals[2] == 1,
                    BitVecVal(1, 1),
                    BitVecVal(0, 1),
                )
            ),
        )

    out_v = BitVecVal(0, 128)
    for i in range(128):
        out_v += (ZeroExt(127, out[i]) << i)

    return z, out_v


def check_flag(flag, res, key):
    fv = BitVecVal(0, 128)
    for i in range(16):
        fv += (ZeroExt(120, flag[i]) << (i * 8))

    fv ^= res

    r = If(fv == key, 1, 0)

    return r


OUTER = {
    "id": "DG4-C",
    "title": "Circular Andromeda",
    "subtitle": "(For internal use only)",
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
            "title": "[redacted]",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "[redacted]",
                    "lines": [
                        {"type": "val", "num": 2, "val": "137457122819891222163237234299646470468"},
                        {"type": "val", "num": 3, "val": "1000000000000"},
                        {"type": "op", "num": 4, "msg": "Complete \"[redacted]\" (DG6) using line 2 for \"Field A\" and line 3 for \"Field B\". Enter the result (DG6, line X) here."}
                    ]
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
                    "title": "[redacted]",
                    "lines": []
                },
                {
                    "num": "Step 2",
                    "title": "Result",
                    "lines": []
                }
            ]
        }
    ]
}

INNER = {
    "id": "DG6",
    "title": "[redacted]",
    "subtitle": "[redacted]",
    "sections": [
        {
            "num": "Part I",
            "title": "[redacted]",
            "type": "general",
            "fields": [
                {"type": "text", "num": 1, "name": "Field A", "info": "internal use only"},
                {"type": "text", "num": 2, "name": "Field B", "info": "internal use only"}
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
                    "lines": []
                },
                {
                    "num": "Step 2",
                    "title": "[redacted]",
                    "lines": []
                },
                {
                    "num": "Step 3",
                    "title": "[redacted]",
                    "lines": []
                }
            ]
        }
    ]
}

def make3(part):
    pre, post = rule_30_step()

    ops = []
    custom = {pre.decl().name(): 'Copy the value in line 1.'}
    flatten_ast(post, [], ops, custom=custom, root=2)
    lines = ops_to_lines(ops)

    m = lines[-1]['num'] + 1

    INNER['sections'][1]['steps'][0]['lines'] = lines

    INNER['sections'][1]['steps'][1]['lines'] = [
        {"type": "op", "num": m, "msg": f"Copy the value from line {m-1}."},
        {"type": "op", "num": m+1, "msg": f"Copy the value from line {2}."},
        {
            "type": "choice",
            "num": m+2,
            "msg": f"Is line {m+1} equal to 0?",
            "yes": "Continue at Step 3.",
            "no": f"Continue at line {m+3}."
        },
        {"type": "val", "num": m+3, "val": -1},
        {"type": "op", "num": m+4, "msg": f"Add line {m+1} and line {m+3}."},
        {"type": "op", "num": m+5, "msg": f"Complete form \"[redacted]\" (DG6) using line {m} for \"Field A\" and line {m+4} for \"Field B\". Enter the result (DG6, line {m+6}) here."}
    ]

    INNER['sections'][1]['steps'][2]['lines'] = [
        {"type": "op", "num": m+6, "msg": f"If you answered \"yes\" to line {m+2}, copy line {m}. Otherwise, copy line {m+5}."}
    ]

    a, b = struct.unpack('<2Q', part)
    flag = ((b << 64) + a)

    # 1 trillion iterations of rule 30
    # see: rule_30_sim.c
    magic = 0x560542730ce1e9ff2a26ad1bc0a15dc

    key = magic ^ flag

    flag = [BitVec('f%d' % i, 8) for i in range(16)]
    res = BitVec('res', 128)
    r = check_flag(flag, res, key)
    ops = []
    custom = {
        flag[i].decl().name(): f'Copy the ASCII value of the character at index {i} of line 1.'
        for i in range(16)
    }
    custom[res.decl().name()] = 'Copy the value from line 4.'
    flatten_ast(r, [], ops, custom=custom, root=4, protect_size=False)
    lines = ops_to_lines(ops)

    m = lines[-1]['num']

    OUTER['sections'][2]['steps'][0]['lines'] = lines

    OUTER['sections'][1]['steps'][0]['lines'][2]['msg'] = f'Complete \"[redacted]\" (DG6) using line 2 for \"Field A\" and line 3 for \"Field B\". Enter the result (DG6, line {m+6}) here.'

    OUTER['sections'][2]['steps'][1]['lines'] = [
        {"type": "op", "num": m+1, "msg": f"Copy the value from line {m}."}
    ]

    open('./builder/forms/DG6.json', 'w').write(json.dumps(INNER))
    open('./builder/forms/DG4-C.json', 'w').write(json.dumps(OUTER))


if __name__=='__main__':
    make3(b'ke_ink_rev3rs1ng')
