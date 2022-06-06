
import hashlib

F1 = b'int3rn4l_r3venue'
F2 = b'_serv1ce_m0re_l1'
F3 = b'ke_ink_rev3rs1ng'
F4 = b'_simul4ti0n_lmao'

print('f1', hashlib.sha256(F1).hexdigest())
print('f2', hashlib.sha256(F2).hexdigest())
print('f3', hashlib.sha256(F3).hexdigest())
print('f4', hashlib.sha256(F4).hexdigest())

FLAG = 'dice{int3rn4l_r3venue_serv1ce_m0re_l1ke_ink_rev3rs1ng_simul4ti0n_lmao}'
