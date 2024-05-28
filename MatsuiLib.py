import array
import random

def generate_bytes_sequence(length, index):
    byte_sequence1 =[int(random.getrandbits(8)) for _ in range(length)]
    byte_sequence2 = byte_sequence1.copy()
    byte_sequence2[index] = byte_sequence1[index] + 1
    return byte_sequence1, byte_sequence2
#wertyuio
def first_modification(K1, K2, k, d):
    K1[d] = K2[d + 1] = k - d - 1

def MaxColStep(K1,K2):
    # Длина списков должна совпадать
    if len(K1) != len(K2):
        return -1
    max_step = 0
    maxcolsteps = 0
    for i in range(len(K1)):
        if K1[i] != K2[i]:
            if max_step <= 2:
                maxcolsteps += 1
                max_step += 1
            else:
                break
        else:
            if max_step <= 2:
                maxcolsteps += 1
            else:
                break

    return maxcolsteps

def K_xy(k, K1, K2):
    d = k - 2
    for x in range(256): #x [0; 255]
        for y in range(1, 256, 1): #y [1; 255]
            if K1[x % k] != K1[d] or K1[x % k] != K1[d + 1]:
                K1[x % k] = (K1[x % k] + y) % 256
                K1[(x + 1) % k] = (K1[(x + 1) % k] - y) % 256
            if K2[x % k] != K2[d] or K2[x % k] != K2[d + 1]:
                K2[x % k] = (K2[x % k] + y) % 256
                K2[(x + 1) % k] = (K2[(x + 1) % k] - y) % 256
    return K1, K2

def max_xy(k, K1, K2):
    max_value = MaxColStep(K1, K2)
    for i in range(k):
        K1modif, K2modif = K_xy(k, K1, K2)
        new_value = MaxColStep(K1modif, K2modif)
        if max_value < new_value:
            max_value = new_value
    return max_value

def search(k, K1, K2):
    p = MaxColStep(K1,K2)
    #print(p)
    # if p == 255:
    #     return 1
    MaxS = max_xy(k, K1, K2)
    #print(MaxS)
    if MaxS <= p:
        return 0
    c = 0
    MaxC = 10
    for i in range(k - 1):
        for j in range(1, k, 1):
            if MaxColStep(K_xy(k, K1, K2)) == MaxS:
                search(k, K_xy(k, K1, K2))
                c += 1
                if c == MaxC:
                    return 1

def find_keys(k, K1, K2):
    count = 0
    while search(k, K1, K2) == 0:
        count += 1
        if search(k, K1, K2) == 1 or count > 10:
            return K1, K2

def bytes_to_uint16_array(data):
    uint16_array = array.array('H')
    uint16_array.frombytes(data)
    return uint16_array
