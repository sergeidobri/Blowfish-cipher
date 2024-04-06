from os import urandom
from random import randint
import blowfish_very_first_py_realization as bl
import unittest


class BlowfishTest(unittest.TestCase):

    def test_ets(self):
        results = []
        num = 8
        for _ in range(1000):
            cnt = randint(4, 56)
            key = b''
            for _ in range(cnt):
                key += urandom(1)
            cipher = bl.BlowCrypt(key)
            block = urandom(num)
            encr_block = b''.join(cipher.encrypt_ets(block))
            decr_block = b''.join(cipher.decrypt_ets(encr_block))
            results.append(decr_block == block)
            num += 8
        assert all(results)

    def test_cbc(self):
        results = []
        num = 8
        for _ in range(1000):
            cnt = randint(4, 56)
            key = b''
            for _ in range(cnt):
                key += urandom(1)
            iv = urandom(8)
            cipher = bl.BlowCrypt(key)
            block = urandom(num)
            encr_block = b''.join(cipher.encrypt_cbc(block, iv))
            decr_block = b''.join(cipher.decrypt_cbc(encr_block, iv))
            results.append(decr_block == block)
            num += 8
        assert all(results)


if __name__ == '__main__':
    unittest.main()


