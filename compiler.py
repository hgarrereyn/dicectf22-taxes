
from z3 import *
import json
import struct


AST_IDX = 0
CONST_CACHE = {}
EXPR_CACHE = {}


def make_json(form_id, title, subtitle, lines):
    m = lines[-1]["num"]
    
    j = json.loads(open('./base_subflag.json', 'r').read())
    
    j['id'] = form_id
    j['title'] = title
    j['subtitle'] = subtitle
    
    j['sections'][1]['steps'][0]['lines'] = lines
    
    j['sections'][1]['steps'][1]['lines'] = [{
        "type": "op",
        "num": m+1,
        "msg": f"Copy the value from line {m}."
    }]

    return j


def compute_target(f, hash_fn):
    s = Solver()
    
    flag = [BitVec('f%d' % d, 8) for d in range(16)]
    for i in range(16):
        s.add(flag[i] == f[i])

    h = hash_fn(flag)

    s.check()
    m = s.model()
    
    return [m.eval(h[i]).as_long() for i in range(len(h))]


def build_checker(f, hash_fn):
    target = compute_target(f, hash_fn)
    
    flag = [BitVec('f%d' % d, 8) for d in range(16)]
    enc = hash_fn(flag)
    
    z = [If(enc[i] == target[i], 1, 0) for i in range(len(enc))]
    s = sum(z)
    v = If(s == len(enc), 1, 0)
    
    return v, flag


def lookup_val(h, ops):
    global CONST_CACHE
    global AST_IDX
    if h in CONST_CACHE:
        return CONST_CACHE[h]
    else:
        AST_IDX += 1
        ops.append((AST_IDX, 'val', h))
        CONST_CACHE[h] = AST_IDX
        return AST_IDX


def flatten_ast(v, flag, ops, custom={}, root=None, protect_size=True):
    global AST_IDX
    global CONST_CACHE
    global EXPR_CACHE
    if root:
        AST_IDX = root
        CONST_CACHE = {}
        EXPR_CACHE = {}
        
    if v.get_id() in EXPR_CACHE:
        return EXPR_CACHE[v.get_id()]

    fname = [x.decl().name() for x in flag]
    
    typ = v.decl().name()
    ch = v.children()
    
    bv_binops = {
        'bvadd': 'add',
        'bvmul': 'mul',
        'bvxor': 'xor',
        'bvand': 'and',
        'bvshl': 'shl',
        'bvashr': 'shr',
        'bvor': 'lor',
        'bvsub': 'sub',
    }
    
    binops = {
        '+': 'add',
        'or': 'or',
    }
    
    if typ in custom:
        AST_IDX += 1
        ops.append((AST_IDX, 'custom', custom[v.decl().name()]))
    elif typ in bv_binops:
        a = flatten_ast(ch[0], flag, ops, custom, protect_size=protect_size)
        b = flatten_ast(ch[1], flag, ops, custom, protect_size=protect_size)
        AST_IDX += 1
        ops.append((AST_IDX, bv_binops[typ], a, b))

        if protect_size:
            # Add an extra binary AND to ensure size
            p = AST_IDX
            h = lookup_val((1 << v.size()) - 1, ops)
            AST_IDX += 1
            ops.append((AST_IDX, 'and', p, h))
    elif typ in binops:
        a = flatten_ast(ch[0], flag, ops, custom, protect_size=protect_size)
        b = flatten_ast(ch[1], flag, ops, custom, protect_size=protect_size)
        AST_IDX += 1
        ops.append((AST_IDX, binops[typ], a, b))
    elif typ == '=':
        a = flatten_ast(ch[0], flag, ops, custom, protect_size=protect_size)
        b = flatten_ast(ch[1], flag, ops, custom, protect_size=protect_size)
        AST_IDX += 1
        ops.append((AST_IDX, 'eq', a, b))
    elif typ in fname:
        AST_IDX += 1
        ops.append((AST_IDX, 'flag', fname.index(typ)))
    elif typ in ['bv', 'Int']:
        h = v.as_long()
        return lookup_val(h, ops)
    elif typ == 'if':
        a = flatten_ast(ch[0], flag, ops, custom, protect_size=protect_size)
        b = flatten_ast(ch[1], flag, ops, custom, protect_size=protect_size)
        c = flatten_ast(ch[2], flag, ops, custom, protect_size=protect_size)
        AST_IDX += 1
        ops.append((AST_IDX, 'if', a, b, c))
    elif typ in ['zero_extend', 'extract']:
        a = flatten_ast(ch[0], flag, ops, custom, protect_size=protect_size)
        return a
    else:
        print(f'Unknown type: [{typ}]')
        return -1
    
    EXPR_CACHE[v.get_id()] = AST_IDX
    return AST_IDX


def ops_to_lines(ops):
    lines = []
    
    for op in ops:
        t = op[1]
        
        if t == 'flag':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Copy the ASCII value of the character at index {op[2]} of line 1."
            })
        elif t == 'custom':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": op[2]
            })
        elif t == 'val':
            lines.append({
                "type": "val",
                "num": op[0],
                "msg": f"(do not modify)",
                "val": str(op[2])
            })
        elif t == 'add':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Add line {op[2]} and line {op[3]}."
            })
        elif t == 'sub':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Subtract line {op[2]} from line {op[3]}."
            })
        elif t == 'xor':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Perform exclusive-or between lines {op[2]} and {op[3]}."
            })
        elif t == 'lor':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Perform logical-or between lines {op[2]} and {op[3]}."
            })
        elif t == 'and':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Perform logical AND between lines {op[2]} and {op[3]}."
            })
        elif t == 'mul':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Multiply line {op[2]} and line {op[3]}."
            })
        elif t == 'shr':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Shift line {op[2]} right by line {op[3]}."
            })
        elif t == 'shl':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"Shift line {op[2]} left by line {op[3]}."
            })
        elif t == 'or':
            lines.append({
                "type": "choice",
                "num": op[0],
                "msg": f"Did you answer \"yes\" to either line {op[2]} or line {op[3]}?",
                "yes": "",
                "no": ""
            })
        elif t == 'eq':
            lines.append({
                "type": "choice",
                "num": op[0],
                "msg": f"Is line {op[2]} equal to line {op[3]}?",
                "yes": "",
                "no": ""
            })
        elif t == 'if':
            lines.append({
                "type": "op",
                "num": op[0],
                "msg": f"If you answered \"yes\" to line {op[2]}, copy the value in line {op[3]}. Otherwise, copy the value in line {op[4]}"
            })
        else:
            print('unknown op', op)
    
    return lines


F1 = 'int3rn4l_r3venue'
F2 = '_serv1ce_m0re_l1'
F3 = 'ke_ink_rev3rs1ng'
F4 = '_simul4ti0n_lmao'

FLAG = b'int3rn4l_r3venue_serv1ce_m0re_l1ke_ink_rev3rs1ng_simul4ti0n_lmao'
