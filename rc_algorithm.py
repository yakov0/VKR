def init_s_box():
    s = list(range(256))
    return s

def swap_elements(i, j, s_box):
    s_box[i], s_box[j] = s_box[j], s_box[i]

def init_s_box_rc4(key):
    s_box = init_s_box()
    j = 0
    for i in range(256):
        j = (j + s_box[i] + key[i % len(key)]) % 256
        #s_box[i], s_box[j] = s_box[j], s_box[i]
        swap_elements(i, j, s_box)
    return s_box

def init_s_box_rc4a():
    s1, s2 = [0]*256, [0]*256
    s_box1 = init_s_box()
    s_box2 = init_s_box()
    j1 = 0
    j2 = 0
    for i in range(256):
        i += 1
        j1 = (j1 + s_box1[i]) % 256
        swap_elements(i, j1, s_box1)
        #s_box1[i], s_box1[j1] = s_box1[j1], s_box1[i]
        i2 = (s_box1[i] + s_box1[j1]) % 256
        s2[i2] = s_box2[i2]
        j2 = (j2 + s_box2[i]) % 256
        swap_elements(i, j2, s_box2)
        #s_box2[i], s_box2[j2] = s_box2[j2], s_box2[i]
        i1 = (s_box2[i] + s_box2[j2]) % 256
        s1[i1] = s_box1[i1]
    return s1, s2

def init_s_box_rc4d(key):
    s_box = init_s_box()
    j = 0
    for i in range(256):
        j = (j + s_box[i + key[i % len(key)]] + key[i % len(key)]) % 256
        #s_box[i], s_box[j] = s_box[j], s_box[i]
        swap_elements(i, j, s_box)
    return s_box




# def generate_bytes_sequence(length, index):
#     length = length // 8
#     byte_sequence1 = []
#     for i in range(length):
#
#     byte_sequence1 = (random.getrandbits(8) for _ in range(length))
#     byte_sequence2 = byte_sequence1.copy()
#     byte_sequence2[index] += 1  # random.randint(0, 255)
#     return byte_sequence1, byte_sequence2
#
# b1, b2 = generate_bytes_sequence(24, 22)
# print(b1, '\n', b2)
