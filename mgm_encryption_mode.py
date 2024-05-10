from kuznechik import kuznyechik_encrypt as enc

n = 128  # длина блока


def addition_of_polinoms(lst1, lst2):
    new_arr = [*map(lambda x: x[0] ^ x[1], zip(lst1, lst2))]
    new_arr = new_arr + max(lst1, lst2, key=len)[len(max(lst1, lst2, key=len)) - (abs(len(lst1) - len(lst2))):]
    return new_arr


def divide_by_primitive_polinom(lst):
    deg, element = 0, 0
    for i in lst[::-1]:
        if i[1]:
            deg = i[0]
            break
    curr_lst2 = [0]*(n+1)
    if n == 128:
        curr_lst2[0], curr_lst2[1], curr_lst2[2], curr_lst2[7], curr_lst2[128] = 1, 1, 1, 1, 1
    elif n == 64:
        curr_lst2[64], curr_lst2[4], curr_lst2[3], curr_lst2[1], curr_lst2[0] = 1, 1, 1, 1, 1
    for _ in range(deg-n):
        curr_lst2.insert(0, 0)
    result = addition_of_polinoms(curr_lst2, [i[1] for i in lst])
    result = result[::-1]
    for _ in range(len(result)):
        if not result[0]:
            del result[0]
            continue
        result = result[::-1]
        break
    if len(result) > n:
        return divide_by_primitive_polinom([(i, el) for i, el in enumerate(result)])
    else:
        return result


def multiply(lst1, lst2):
    lst1 = [*map(int, list(lst1[::-1]))]
    lst2 = [*map(int, list(lst2[::-1]))]
    result = []
    for ind, el in enumerate(lst1):
        curr_lst2 = lst2[:]
        if el:
            for _ in range(ind):
                curr_lst2.insert(0, 0)
            result = addition_of_polinoms(result, curr_lst2)
    if len(result) > n:
        result = divide_by_primitive_polinom([(i, el) for i, el in enumerate(result)])
    return '0' * (n - len(result)) + ''.join(map(str, result[::-1]))


# num - 16 сс
def incr_left(num):
    mid = len(num) // 2
    left = num[:mid]
    right = num[mid:]
    left = hex((int(left, 16) + 1) % 2**(n//2))[2:].rjust(mid, '0')
    return left + right


# num - 16 cc
def incr_right(num):
    mid = len(num) // 2
    left = num[:mid]
    right = num[mid:]
    right = hex((int(right, 16) + 1) % 2**(n//2))[2:].rjust(mid, '0')
    return left + right


key = int('8899AABBCCDDEEFF0011223344556677FEDCBA98765432100123456789ABCDEF', 16)
nonce = '1122334455667700FFEEDDCCBBAA9988'
plaintext = '1122334455667700FFEEDDCCBBAA998800112233445566778899AABBCCEEFF0A112233445566778899AABBCCEEFF0A002233445566778899AABBCCEEFF0A0011AABBCC'
protected_data = '0202020202020202010101010101010104040404040404040303030303030303EA0505050505050505'

nonce = bin(int(nonce, 16))[2:].rjust(n-1, '0')

nonce_to_encrypt = int(('0' + nonce), 2)
gammas = []
cipher_text = []

for i in range(0, len(plaintext), n//4):
    if not gammas:
        gammas.append(enc(nonce_to_encrypt, key))
        cipher_text.append(hex(int(enc(int(gammas[-1], 16), key), 16) ^ int(plaintext[i:i+n//4], 16))[2:])
        continue
    gammas.append(incr_right(gammas[-1]))
    if len(plaintext[i:i+n//4]) == n//4:
        cipher_text.append(hex(int(enc(int(gammas[-1], 16), key), 16) ^ int(plaintext[i:i + n//4], 16))[2:])
    else:
        curr_plaintext_block = plaintext[i:i+n//4]
        curr_len_block = len(curr_plaintext_block)
        while len(curr_plaintext_block) != n//4:
            curr_plaintext_block += '0'
        cipher_text.append(hex(int(enc(int(gammas[-1], 16), key), 16) ^ int(curr_plaintext_block, 16))[2:][:curr_len_block])

cipher_text_res = ''.join(cipher_text)


cnt = (len(protected_data) // (n//4) + (len(protected_data) % (n//4) != 0)) + (len(cipher_text_res) // (n//4) + (len(cipher_text_res) % (n//4) != 0)) + 1  # h + q + 1. h- количество блоков имитозащищаемых данных, q - количество блоков шифртекста
Zs = []
Hs = []
nonce_to_encrypt = int('1' + nonce, 2)
for i in range(cnt):
    if not Zs:
        Zs.append(enc(nonce_to_encrypt, key))
        Hs.append(enc(int(Zs[-1], 16), key))
        continue
    Zs.append(incr_left(Zs[-1]))
    Hs.append(enc(int(Zs[-1], 16), key))


j = 0
result_T = 0
for i in range(0, len(protected_data), n//4):
    curr_block_protected_data = protected_data[i:i+n//4]
    while len(curr_block_protected_data) != n//4:
        curr_block_protected_data += '0'
    result_T ^= int(multiply(bin(int(curr_block_protected_data, 16))[2:], bin(int(Hs[j], 16))[2:]), 2)
    j += 1

for i in range(0, len(cipher_text_res), n//4):
    curr_block_cipher_text_res = cipher_text_res[i:i+n//4]
    while len(curr_block_cipher_text_res) != n//4:
        curr_block_cipher_text_res += '0'
    result_T ^= int(multiply(bin(int(curr_block_cipher_text_res, 16))[2:], bin(int(Hs[j], 16))[2:]), 2)
    j += 1

lenA = hex(len(protected_data)//2 * 8)[2:]
lenC = hex(len(cipher_text_res)//2 * 8)[2:]

lenA_lenC = lenA.rjust(n//8, '0') + lenC.rjust(n//8, '0')

result_T ^= int(multiply(bin(int(lenA_lenC, 16))[2:], bin(int(Hs[j], 16))[2:]), 2)
result_T = enc(result_T, key)

print(f'Результат шифрования:\n1. nonce: {hex(int(nonce, 2))[2:]}\n2. Дополнительные имитозащищаемые данные: {protected_data.lower()}\n3. Шифротекст: {cipher_text_res}\n4. Имитовставка Т: {result_T}')


key = int('8899AABBCCDDEEFF0011223344556677FEDCBA98765432100123456789ABCDEF', 16)
nonce = '1122334455667700FFEEDDCCBBAA9988'
ciphertext = 'a9757b8147956e9055b8a33de89f42fc8075d2212bf9fd5bd3f7069aadc16b39497ab15915a6ba85936b5d0ea9f6851cc60c14d4d3f883d0ab94420695c76deb2c7552'
protected_data = '0202020202020202010101010101010104040404040404040303030303030303EA0505050505050505'
T = 'cf5d656f40c34f5c46e8bb0e29fcdb4c'


nonce = bin(int(nonce, 16))[2:].rjust(n-1, '0')

cnt = (len(protected_data) // (n//4) + (len(protected_data) % (n//4) != 0)) + (len(ciphertext) // (n//4) + (len(ciphertext) % (n//4) != 0)) + 1  # h + q + 1. h- количество блоков имитозащищаемых данных, q - количество блоков шифртекста
Zs = []
Hs = []
nonce_to_encrypt = int('1' + nonce, 2)
for i in range(cnt):
    if not Zs:
        Zs.append(enc(nonce_to_encrypt, key))
        Hs.append(enc(int(Zs[-1], 16), key))
        continue
    Zs.append(incr_left(Zs[-1]))
    Hs.append(enc(int(Zs[-1], 16), key))

lenA = hex(len(protected_data)//2 * 8)[2:]
lenC = hex(len(ciphertext)//2 * 8)[2:]

lenA_lenC = lenA.rjust(n//8, '0') + lenC.rjust(n//8, '0')


result_T = 0
j = 0
for i in range(0, len(protected_data), n//4):
    curr_block_protected_data = protected_data[i:i+n//4]
    while len(curr_block_protected_data) != n//4:
        curr_block_protected_data += '0'
    result_T ^= int(multiply(bin(int(curr_block_protected_data, 16))[2:], bin(int(Hs[j], 16))[2:]), 2)
    j += 1

for i in range(0, len(ciphertext), n//4):
    curr_block_ciphertext = ciphertext[i:i+n//4]
    while len(curr_block_ciphertext) != n//4:
        curr_block_ciphertext += '0'
    result_T ^= int(multiply(bin(int(curr_block_ciphertext, 16))[2:], bin(int(Hs[j], 16))[2:]), 2)
    j += 1


result_T ^= int(multiply(bin(int(lenA_lenC, 16))[2:], bin(int(Hs[j], 16))[2:]), 2)
result_T = enc(result_T, key)

if result_T != T:
    raise ValueError('Значение имитовставки отличается от той, с помощью которой был зашифрован текст')

nonce_to_encrypt = int('0' + nonce, 2)
gammas = [enc(nonce_to_encrypt, key)]
plaintext = ''

for i in range(0, len(ciphertext), n//4):
    curr_block_ciphertext = ciphertext[i:i+n//4]
    while len(curr_block_ciphertext) != n//4:
        curr_block_ciphertext += '0'
    plaintext += hex(int(enc(int(gammas[-1], 16), key), 16) ^ int(curr_block_ciphertext, 16))[2:].rjust(n//4, '0')
    gammas.append(incr_right(gammas[-1]))

plaintext = plaintext[:len(ciphertext)]
print(f'Результат расшифрования:\n1. Открытый текст: {plaintext}\n2. Дополнительные имитозащищаемые данные: {protected_data.lower()}')
