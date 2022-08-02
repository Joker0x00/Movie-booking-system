# Author: wy
# Time: 2022/7/2 16:36

import hashlib


def md5(str):
    h1 = hashlib.md5()
    h1.update(str.encode(encoding='utf-8'))
    return h1.hexdigest()