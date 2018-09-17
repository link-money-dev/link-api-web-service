import hashlib

def get_md5(str):
    md5=hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
    md5=str(md5).upper()
    return
