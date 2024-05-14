import blowfish_very_first_py_realization as bl
import unittest
import gostcrypto
import cubehash as cb

# Tests for blowfish: https://www.schneier.com/wp-content/uploads/2015/12/vectors-2.txt
# Tests for mgm: https://meganorm.ru/Data2/1/4293727/4293727270.pdf
# Tests for cubehash: https://en.wikipedia.org/wiki/CubeHash


def bytes_to_hex(num):
    res = ''
    for i in num:
        res += hex(i)[2:].rjust(2, '0')
    return res


class BlowfishTest(unittest.TestCase):

    def setUp(self):
        h_to_b = self.hex_str_to_bytes
        self.vectors_ets, self.vectors_mgm = self.load_vectors()
        self.test_key = h_to_b('112233445566778899112233445566778899')
        self.test_initializing_vector = h_to_b('1122334455667788')
        self.test_nonce = h_to_b('12DEF06B3C130A59')
        self.test_protected_data = h_to_b('01010101010101010202020202020202030303030303030304040404040404040505050505050505EA')

    def load_vectors(self):
        vectors = []
        vectors_mgm = []
        with open('data_for_tests/blowfish_vectors', 'r') as file:
            flag_mgm = False
            for line in file.readlines():
                if line.strip() == 'MGM Magma':
                    flag_mgm = True
                    continue
                if flag_mgm:
                    key, nonce, protected_data, clear_bytes, cipher_bytes, cipher_T = map(self.hex_str_to_bytes, line.split())
                    vectors_mgm.append((key, nonce, protected_data, clear_bytes, cipher_bytes, cipher_T))
                    continue
                key, clear_bytes, cipher_bytes = map(self.hex_str_to_bytes, line.split())
                vectors.append((key, clear_bytes, cipher_bytes))
        return vectors, vectors_mgm

    def test_ets_encrypt_decrypt_1_block(self):
        key = self.test_key
        EncryptObject = bl.BlowCrypt(key)
        # 1 block:
        with open('data_for_tests/blowfish_testing_1_block', 'rb') as bl1:
            block_1 = bl1.read().strip()
            my_bytes = b''.join(EncryptObject.encrypt_ets(block_1))
            my_decrypted_bytes = b''.join(EncryptObject.decrypt_ets(my_bytes))

            self.assertEqual(my_decrypted_bytes, block_1)

    def test_ets_encrypt_decrypt_1000_blocks(self):
        key = self.test_key
        EncryptObject = bl.BlowCrypt(key)
        # 1_000 blocks:
        with open('data_for_tests/blowfish_testing_1000_blocks', 'rb') as bl1000:
            block_1000 = bl1000.read().strip()
            my_bytes = b''.join(EncryptObject.encrypt_ets(block_1000))
            my_decrypted_bytes = b''.join(EncryptObject.decrypt_ets(my_bytes))

            self.assertEqual(my_decrypted_bytes, block_1000)

    def test_ets_encrypt_decrypt_1000000_blocks(self):
        key = self.test_key
        EncryptObject = bl.BlowCrypt(key)
        # 1_000_000 blocks:
        with open('data_for_tests/blowfish_testing_1000000_blocks', 'rb') as bl1000000:
            block_1000000 = bl1000000.read().strip()
            my_bytes = b''.join(EncryptObject.encrypt_ets(block_1000000))
            my_decrypted_bytes = b''.join(EncryptObject.decrypt_ets(my_bytes))

            self.assertEqual(my_decrypted_bytes, block_1000000)

    def test_ets_specification_vectors(self):
        for key, clear_bytes, cipher_bytes in self.vectors_ets:
            my_bytes = b''.join(bl.BlowCrypt(key).encrypt_ets(clear_bytes))
            self.assertEqual(my_bytes, cipher_bytes)

            self.assertEqual(b''.join(bl.BlowCrypt(key).decrypt_ets(my_bytes)), clear_bytes)

    def test_cbc_encrypt_decrypt_1_block(self):
        key = self.test_key
        iv = self.test_initializing_vector
        EncryptObject = bl.BlowCrypt(key)
        # 1 block:
        with open('data_for_tests/blowfish_testing_1_block', 'rb') as bl1:
            block_1 = bl1.read().strip()
            my_bytes = b''.join(EncryptObject.encrypt_cbc(block_1, iv))
            my_decrypted_bytes = b''.join(EncryptObject.decrypt_cbc(my_bytes, iv))

            self.assertEqual(my_decrypted_bytes, block_1)

    def test_cbc_encrypt_decrypt_1000_blocks(self):
        key = self.test_key
        iv = self.test_initializing_vector
        EncryptObject = bl.BlowCrypt(key)
        # 1_000 blocks:
        with open('data_for_tests/blowfish_testing_1000_blocks', 'rb') as bl1000:
            block_1000 = bl1000.read().strip()
            my_bytes = b''.join(EncryptObject.encrypt_cbc(block_1000, iv))
            my_decrypted_bytes = b''.join(EncryptObject.decrypt_cbc(my_bytes, iv))

            self.assertEqual(my_decrypted_bytes, block_1000)

    def test_cbc_encrypt_decrypt_1000000_block(self):
        key = self.test_key
        iv = self.test_initializing_vector
        EncryptObject = bl.BlowCrypt(key)
        # 1_000_000 blocks:
        with open('data_for_tests/blowfish_testing_1000000_blocks', 'rb') as bl1000000:
            block_1000000 = bl1000000.read().strip()
            my_bytes = b''.join(EncryptObject.encrypt_cbc(block_1000000, iv))
            my_decrypted_bytes = b''.join(EncryptObject.decrypt_cbc(my_bytes, iv))

            self.assertEqual(my_decrypted_bytes, block_1000000)

    def test_mgm_specification_vectors(self):
        key, nonce, protected_data, clear_bytes, cipher_bytes, cipher_T = self.vectors_mgm[0]
        EncryptObject = bl.BlowCrypt(key)
        EncryptObject.encr_object = cipher_object = gostcrypto.gostcipher.new('magma', key, gostcrypto.gostcipher.MODE_ECB)
        EncryptObject.encrypt = cipher_object.encrypt

        res = EncryptObject.encrypt_mgm(nonce, clear_bytes, protected_data)
        my_bytes = res[2]
        my_T = res[3]
        self.assertEqual(my_bytes, cipher_bytes)
        self.assertEqual(my_T, cipher_T)

        res = EncryptObject.decrypt_mgm(nonce, my_bytes, protected_data, cipher_T)
        my_decrypted_bytes = res[0]
        self.assertEqual(my_decrypted_bytes, clear_bytes)

    def test_mgm_encrypt_decrypt_1_block(self):
        key = self.test_key
        nonce = self.test_nonce
        protected_data = self.test_protected_data
        EncryptObject = bl.BlowCrypt(key)
        # 1 block:
        with open('data_for_tests/blowfish_testing_1_block', 'rb') as bl1:
            block_1 = bl1.read().strip()
            res_encr = EncryptObject.encrypt_mgm(nonce, block_1, protected_data)
            my_bytes = res_encr[2]
            my_T = res_encr[3]
            res_decr = EncryptObject.decrypt_mgm(nonce, my_bytes, protected_data, my_T)
            my_decrypted_bytes = res_decr[0]

            self.assertEqual(my_decrypted_bytes, block_1)

    def test_mgm_encrypt_decrypt_1000_blocks(self):
        key = self.test_key
        nonce = self.test_nonce
        protected_data = self.test_protected_data
        EncryptObject = bl.BlowCrypt(key)
        # 1_000 blocks:
        with open('data_for_tests/blowfish_testing_1000_blocks', 'rb') as bl1000:
            block_1000 = bl1000.read().strip()
            res_encr = EncryptObject.encrypt_mgm(nonce, block_1000, protected_data)
            my_bytes = res_encr[2]
            my_T = res_encr[3]
            res_decr = EncryptObject.decrypt_mgm(nonce, my_bytes, protected_data, my_T)
            my_decrypted_bytes = res_decr[0]

            self.assertEqual(my_decrypted_bytes, block_1000)

    def test_mgm_encrypt_decrypt_1000000_blocks(self):
        key = self.test_key
        nonce = self.test_nonce
        protected_data = self.test_protected_data
        EncryptObject = bl.BlowCrypt(key)
        # 1_000_000 blocks:
        with open('data_for_tests/blowfish_testing_1000000_blocks', 'rb') as bl1000000:
            block_1000000 = bl1000000.read().strip()
            res_encr = EncryptObject.encrypt_mgm(nonce, block_1000000, protected_data)
            my_bytes = res_encr[2]
            my_T = res_encr[3]
            res_decr = EncryptObject.decrypt_mgm(nonce, my_bytes, protected_data, my_T)
            my_decrypted_bytes = res_decr[0]

            self.assertEqual(my_decrypted_bytes, block_1000000)

    @staticmethod
    def hex_str_to_bytes(data):
        res = b''
        for i in range(0, len(data), 2):
            res += int(data[i:i+2], 16).to_bytes(1)
        return res


class CubeHashTest(unittest.TestCase):
    def setUp(self):
        self.hashes, self.initial_states = self.load_hashes()
        print(self.hashes)
        print(self.initial_states)

    def load_hashes(self):
        flag_hash = False
        initial_states = []
        hashes = []
        with open('data_for_tests/cubehash_vectors', 'r') as file:
            lines = [*map(lambda l: l.strip(), file.readlines())]
            for line in lines:
                if line == 'initial':
                    continue
                elif line == 'hash':
                    flag_hash = True
                    continue
                if flag_hash:
                    i, r, b, f, h, message, hash_result = line.split('_')
                    i, r, b, f, h = int(i), int(r), int(b), int(f), int(h)
                    if message == 'zero-string':
                        message = ''
                    hashes.append((i, r, b, f, h, message, hash_result))
                    continue
                i, r, b, f, h, initial_state = line.split('_')
                i, r, b, f, h = int(i), int(r), int(b), int(f), int(h)
                initial_states.append((i, r, b, f, h, initial_state))
        return hashes, initial_states

    def test_initialize_wiki_tests(self):
        for (i, r, b, f, h, initial_state) in self.initial_states:
            my_init = cb.CubeHash(i, r, b, f, h).get_state_for_check()

            self.assertEqual(my_init, initial_state)

    def test_hashing_wiki_tests(self):
        for (i, r, b, f, h, message, hash_result) in self.hashes:
            my_hash = cb.CubeHash(i, r, b, f, h).hash(message)

            self.assertEqual(my_hash, hash_result)

    def test_speed_of_hashing_1_block(self):
        # i, r, b, f, h were taken from the main specification of algorithm: https://cubehash.cr.yp.to/index.html
        with open('data_for_tests/cubehash_testing_1_block', 'r') as file:
            cb.CubeHash(16, 16, 32, 32, 512).hash(file.read())

    def test_speed_of_hashing_1000_blocks(self):
        # i, r, b, f, h were taken from the main specification of algorithm: https://cubehash.cr.yp.to/index.html
        with open('data_for_tests/cubehash_testing_1000_blocks', 'r') as file:
            cb.CubeHash(16, 16, 32, 32, 512).hash(file.read())

    def test_speed_of_hashing_1000000_blocks(self):
        # i, r, b, f, h were taken from the main specification of algorithm: https://cubehash.cr.yp.to/index.html
        with open('data_for_tests/cubehash_testing_1000000_blocks', 'r') as file:
            cb.CubeHash(16, 16, 32, 32, 512).hash(file.read())


if __name__ == '__main__':
    unittest.main()
