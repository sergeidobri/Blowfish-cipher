def num_to_bits(num, width):
    bin_num = bin(num)[2:]
    return f'{bin_num}'.rjust(width, '0')


def finalize(state_in, f):
    xored = state_in[-1] ^ 1
    res_str = state_in[:-1] + xored.to_bytes(1)

    return transform(res_str, f)


def xor(n1, n2):
    b = len(n2)
    res = b''
    for i in range(b):
        res += (n2[i] ^ n1[i]).to_bytes(1)
    for i in range(b, len(n1)):
        res += n1[i].to_bytes(1)
    return res


# def transform(state_in, times):
#     state_lst = []  # так как во время трансформации работа идет непосредственно с 32-умя 4-ех байтовыми словами, мы должны группы по 4 байта объединить в одно слово
#     for e in range(0, 128, 4):
#         curr_num = state_in[e:e+4]
#         state_lst.append(int.from_bytes(curr_num, 'little'))
#
#     for _ in range(times):  # проводим столько раундов, сколько указываем функции вторым аргументом
#
#         # 1. modulo 2^32
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     for m in range(2):
#                         state_lst[2**4 + j*2**3 + k*2**2 + l*2 + m] = (state_lst[j*2**3 + k*2**2 + l*2 + m] + state_lst[2**4 + j*2**3 + k*2**2 + l*2 + m]) % 2**32  # слово x[1jklm] складываем по модулю 2^32 с x[0jklm]
#
#         # 2. rotate left by 7 bits
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     for m in range(2):
#                         x = state_lst[j*2**3 + k*2**2 + l*2 + m]  # элемент x[0jklm] присваем переменной x
#                         x_byte = x.to_bytes(4, 'little')  # слово x[0jklm] переводим в байты, порядок которых: little
#                         bytes_lst = [num_to_bits(byte, 8) for byte in x_byte]  # каждый байт переводим в биты, записываем их в список
#                         x_str = ''.join(bytes_lst)  # все байты, представленные в виде битов, соединяем в единое слово. Мы получили x[0jklm], представленный битами, с учетом того, что порядок следования байтов: little endian
#                         x_str_rotated = x_str[7:] + x_str[:7]  # выполняем сдвиг влево на 7 битов
#                         x_final = int.from_bytes(b''.join([int(x_str_rotated[r:r+8], 2).to_bytes(1) for r in range(0, len(x_str_rotated), 8)]), 'little')  # после сдвига оставляем этот элемент в виде целого числа с учетом порядка байтов little endian
#                         state_lst[j * 2 ** 3 + k * 2 ** 2 + l * 2 + m] = x_final
#
#         # 3. swapping
#         for k in range(2):
#             for l in range(2):
#                 for m in range(2):
#                     state_lst[k*2**2 + l*2 + m], state_lst[2**3 + k*2**2 + l*2 + m] = state_lst[2**3 + k*2**2 + l*2 + m], state_lst[k*2**2 + l*2 + m]  # слово x[00klm] меняем местами с x[01klm]
#
#         # 4. xor
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     for m in range(2):  # в силу того, что наши слова представляют собой 4-байтовые последовательности, операция xor не зависит от порядка следования их байтов. Важно только, чтобы порядки их следования были одинаковые. В нашем же случае: little и little
#                         state_lst[j*2**3 + k*2**2 + l*2 + m] ^= state_lst[2**4 + j*2**3 + k*2**2 + l*2 + m]  # проводим операцию xor над элементами x[0jklm] и x[1jklm] и присваиваем результат x[0jklm]
#
#         # 5. swap
#         for j in range(2):
#             for k in range(2):
#                 for m in range(2):
#                     state_lst[2**4 + j*2**3 + k*2**2 + m], state_lst[2**4 + j*2**3 + k*2**2 + 2 + m] = state_lst[2**4 + j*2**3 + k*2**2 + 2 + m], state_lst[2**4 + j*2**3 + k*2**2 + m]  # меняем местами элементы x[1jk0m] и x[1jk1m]
#
#         # 6. modulo 2^32
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     for m in range(2):
#                         state_lst[2**4 + j*2**3 + k*2**2 + l*2 + m] = (state_lst[j*2**3 + k*2**2 + l*2 + m] + state_lst[2**4 + j*2**3 + k*2**2 + l*2 + m]) % 2**32  # сложить по модулю 2^32 x[1jklm] с x[0jklm] и присвоить это x[1jklm]
#
#         # 7. rotate left by 11 bits
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     for m in range(2):
#                         x = state_lst[j*2**3 + k*2**2 + l*2 + m]  # присваиваем x[0jklm] переменной x
#                         x_byte = x.to_bytes(4, 'little')  # переводим число в байты, с учетом порядка little endian
#                         bytes_lst = [num_to_bits(byte, 8) for byte in x_byte]  # переводим байты в биты и сохряняем их в списке
#                         x_str = ''.join(bytes_lst)  # все биты, что мы сохранили, соединяем в одну строку. Мы получили число x[0jklm], представленный в виде битов, с учетом порядка следования байтов little endian
#                         x_str_rotated = x_str[11:] + x_str[:11]  # производим сдвиг на 11 битов влево по кругу
#                         x_final = int.from_bytes(b''.join([int(x_str_rotated[r:r+8], 2).to_bytes(1) for r in range(0, len(x_str_rotated), 8)]), 'little')  # переводим число из битов в байты обратно, с учетом следования байтов в порядке little endian
#                         state_lst[j * 2 ** 3 + k * 2 ** 2 + l * 2 + m] = x_final  # присваем получившееся целое число элементу x[0jklm]
#
#         # 8. swap
#         for j in range(2):
#             for l in range(2):
#                 for m in range(2):
#                     state_lst[j*2**3 + l*2 + m], state_lst[j*2**3 + 2**2 + l*2 + m] = state_lst[j*2**3 + 2**2 + l*2 + m], state_lst[j*2**3 + l*2 + m]  # меняем местами слова x[0j0km] и x[0j1lm]
#
#         # 9. xor
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     for m in range(2):
#                         state_lst[j*2**3 + k*2**2 + l*2 + m] ^= state_lst[2**4 + j*2**3 + k*2**2 + l*2 + m]  # x[0jklm] = x[0jklm] ^ x[1jklm] (4-ый шаг повтор)
#
#         # 10. swap
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     state_lst[2**4 + j*2**3 + k*2**2 + l*2], state_lst[2**4 + j*2**3 + k*2**2 + l*2 + 1] = state_lst[2**4 + j*2**3 + k*2**2 + l*2 + 1], state_lst[2**4 + j*2**3 + k*2**2 + l*2]  # меняем местами слова x[1jkl0] и x[1jkl1]
#
#     res_str = b''  # вывод этой функции мы дадим в виде байтовой строки. То есть так же, как и был дан ввод
#     for e in range(32):
#         res_str += state_lst[e].to_bytes(4, 'little')
#     return res_str


def transform(state_in, times):
    x = [state_in[i:i+4] for i in range(0, len(state_in), 4)]

    for _ in range(times):
        #1. modulo
        for i in range(16):
            # print(x[i^16], x[i])
            # print(int.from_bytes(x[i^16], 'little'), int.from_bytes(x[i], 'little'))
            # print(int.from_bytes(x[i^16], 'little') + int.from_bytes(x[i], 'little'))
            # print((int.from_bytes(x[i ^ 16], 'little') + int.from_bytes(x[i], 'little')) % 2**32)
            x[i^16] = int((int.from_bytes(x[i^16], 'little') + int.from_bytes(x[i], 'little')) % (2**32)).to_bytes(4, 'little')

        #2. rotation
        for i in range(16):
            el = x[i]
            el_bits = ''.join([num_to_bits(j, 8) for j in el])
            el_bits = el_bits[7:] + el_bits[:7]
            x[i] = b''.join([int(el_bits[j:j+8], 2).to_bytes(1) for j in range(0, len(el_bits), 8)])


        #3. swap
        for i in range(8):
            x[i], x[i^8] = x[i^8], x[i]


        #4. xor
        for i in range(16):
            x[i] = (int.from_bytes(x[i^16], 'little') ^ int.from_bytes(x[i], 'little')).to_bytes(4, 'little')

        #5. swap
        for i in [16, 17, 20, 21, 24, 25, 28, 29]:
            x[i], x[i^2] = x[i^2], x[i]

        # 6. modulo
        for i in range(16):
            x[i ^ 16] = int((int.from_bytes(x[i ^ 16], 'little') + int.from_bytes(x[i], 'little')) % 2 ** 32).to_bytes(4, 'little')


        #7. rotation
        for i in range(16):
            el = x[i]
            el_bits = ''.join([num_to_bits(j, 8) for j in el])
            el_bits = el_bits[11:] + el_bits[:11]
            x[i] = b''.join([int(el_bits[j:j+8], 2).to_bytes(1) for j in range(0, len(el_bits), 8)])

        #8. swap
        for i in [0, 1, 2, 3, 8, 9, 10, 11]:
            x[i], x[i^4] = x[i^4], x[i]

        #9. xor
        for i in range(16):
            x[i] = (int.from_bytes(x[i^16], 'little') ^ int.from_bytes(x[i], 'little')).to_bytes(4, 'little')

        #10. swap
        for i in [16, 18, 20, 22, 24, 26, 28, 30]:
            x[i], x[i+1] = x[i+1], x[i]

    return b''.join(x)

# I = 16  # количество раундов для инициализации state-a
r = 8  # количество раундов на одну трансформацию state-a
I = 10*r
b = 1  # количество байтов, которые мы будем считать одним блоком
# f = 32  # количество раундов финализации. Перед выводом хеша мы будем еще f раз трансформировать state
f = 10*r
h = 256  # количество выводимых битов


state = b''  # инициализируем state как байтовую строку
for i in [h//8, b, r]:
    state += i.to_bytes(4, 'little')  # устанавливаем первые 3 4-байтовых слова как h//8, b, r соответственно
while len(state) != 128:
    state += int(0).to_bytes(1)  # дополняем оставшиеся 29 слов 0-выми словами. Они содержат каждый по 4 байта \x00, поэтому просто прибавляем 0-вые байты, пока длина не станет равна 128
print(state)
state = transform(state, I)  # трансформируем state I раз
print(''.join(map(lambda x: hex(x)[2:], state)))

message = input('Введите хрень: ').encode()
message_bits = ''.join([num_to_bits(i, 8) for i in message])  # переводим введенные данные в биты, дописываем 1 в конце и добиваем нулями, пока кол-во не будет делиться нацело на 8b
message_bits += '1'
while len(message_bits) % (8*b) != 0:
    message_bits += '0'

message = b''.join([int(message_bits[i:i+8], 2).to_bytes(1) for i in range(0, len(message_bits), 8)])  # переводим биты в байты

for k in range(0, len(message), b):
    state = xor(state, message[k:k+b])
    state = transform(state, r)

hello = '7ce309a25e2e1603ca0fc369267b4d43f0b1b744ac45d6213ca08e75675664448e2f62fdbf7bbd637ce40fc293286d75b9d09e8dda31bd029113e02ecccfd39b'

state = finalize(state, f)
final_hash = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), state))
print(final_hash == hello)
