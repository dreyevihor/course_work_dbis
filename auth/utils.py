from hashlib import md5

__all__ = ('get_password_hash', 'check_password')


def get_password_hash(password):
    return md5(bytes(password)).hexdigest()

def check_password(password, hash):
    return md5(bytes(password)).hexdigest() == hash