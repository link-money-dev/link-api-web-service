def sortedDictValues3(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

def check_validity_of_address(address):
    try:
        address=str(address)
        if len(address) != 56:
            return False
        elif address.upper() != address:
            return False
        elif address[0] != 'G':
            return False
        else:
            return True
    except:
        return False

import hashlib
from wrapper import encryption
def check_hash(d, cypher, method='md5'):
    copy_d={}
    copy_d['order']
    if method.lower()=='md5':
        _cypher = str(hashlib.md5(d.encode('utf-8')).hexdigest()).upper()
        if cypher==_cypher:
            return True
        else:
            return False
    if method.lower()=='aes':
        prp=encryption.Prpcrypt()
        _cypher=str()