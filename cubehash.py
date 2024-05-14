class CubeHash:
    def __init__(self, i, r, b, f, h):
        self.i = i
        self.r = r
        self.b = b
        self.f = f
        self.h = h
        transform = self._transform
        state = [h//8, b, r]
        while len(state) != 32:
            state.append(0)
        state = transform(state, i)
        self.state = state
        state_for_check = [int.from_bytes(state[i:i+4], 'little') for i in range(0, len(state), 4)]
        state_for_check = b''.join(map(lambda x: int(x).to_bytes(4), state_for_check))
        self.state_for_check = state_for_check

    def hash(self, message):
        b = self.b
        r = self.r
        f = self.f
        h = self.h
        state = self.state
        transform = self._transform

        message = message.encode()

        if message:
            message = bin(int.from_bytes(message))[2:].rjust(8 * len(message), '0')
        else:
            message = ''
        message += '1'
        while len(message) % (8 * b) != 0:
            message += '0'
        message = b''.join([int(message[i:i + 8], 2).to_bytes(1) for i in range(0, len(message), 8)])

        for k in range(0, len(message), b):
            state = list(state)
            for j in range(0, b):
                state[j] ^= message[k + j]
            state = b''.join([int(i).to_bytes(1) for i in state])
            state = transform(state, r)

        state = [int.from_bytes(state[i:i + 4], 'little') for i in range(0, len(state), 4)]
        state[31] ^= 1
        state = transform(state, f)
        final_hash = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), state[:h // 8]))
        return final_hash

    def get_state_for_check(self):
        return ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), self.state_for_check))

    def _transform(self, state_in, times):
        rotate_left = self._rotate_left

        if isinstance(state_in, list):
            x = state_in[:]
        else:
            x = [int.from_bytes(state_in[i:i + 4], 'little') for i in range(0, len(state_in), 4)]

        for _ in range(times):
            # 1. modulo
            for i in range(16):
                x[i ^ 16] = (x[i ^ 16] + x[i]) % (2 ** 32)

            # 2. rotation
            for i in range(16):
                x[i] = rotate_left(x[i], 7)

            # 3. swap
            for i in range(8):
                x[i], x[i ^ 8] = x[i ^ 8], x[i]

            # 4. xor
            for i in range(16):
                x[i] ^= x[i ^ 16]

            # 5. swap
            for i in [16, 17, 20, 21, 24, 25, 28, 29]:
                x[i], x[i ^ 2] = x[i ^ 2], x[i]

            # 6. modulo
            for i in range(16):
                x[i ^ 16] = (x[i ^ 16] + x[i]) % (2 ** 32)

            # 7. rotation
            for i in range(16):
                x[i] = rotate_left(x[i], 11)

            # 8. swap
            for i in [0, 1, 2, 3, 8, 9, 10, 11]:
                x[i], x[i ^ 4] = x[i ^ 4], x[i]

            # 9. xor
            for i in range(16):
                x[i] ^= x[i ^ 16]

            # 10. swap
            for i in [16, 18, 20, 22, 24, 26, 28, 30]:
                x[i], x[i + 1] = x[i + 1], x[i]

        res = b''
        for i in x:
            res += int(i).to_bytes(4, 'little')

        return res

    @staticmethod
    def _rotate_left(number, rotation):
        rotation %= 32
        return ((number << rotation) | (number >> (32 - rotation))) & 0xffffffff