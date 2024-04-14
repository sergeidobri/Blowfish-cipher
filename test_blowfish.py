import blowfish_very_first_py_realization as bl
import unittest


class BlowfishTest(unittest.TestCase):

    def setUp(self):
        self.vectors = self.load_vectors()

    def load_vectors(self):
        vectors = []
        with open('blowfish_vectors', 'r') as file:
            for line in file.readlines():
                key, clear_bytes, cipher_bytes = map(self.hex_str_to_bytes, line.split())
                vectors.append((key, clear_bytes, cipher_bytes))
        return vectors

    def test_ets_encrypt_decrypt(self):
        for key, clear_bytes, cipher_bytes in self.vectors:
            my_bytes = b''.join(bl.BlowCrypt(key).encrypt_ets(clear_bytes))
            self.assertEqual(my_bytes, cipher_bytes)

            self.assertEqual(b''.join(bl.BlowCrypt(key).decrypt_ets(my_bytes)), clear_bytes)


    @staticmethod
    def hex_str_to_bytes(data):
        res = b''
        for i in range(0, len(data), 2):
            res += int(data[i:i+2], 16).to_bytes()
        return res


if __name__ == '__main__':
    unittest.main()
