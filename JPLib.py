import random
import rc_algorithm as rc

def generate_bytes_sequence(length, index):
    byte_sequence =[int(random.getrandbits(8)) for _ in range(length)]
    return byte_sequence

def store_j(k):
    d = k - 3
    n = (256 + k - 1 - d) // k
    J = []
    for i in range (d + k - 2, d + k * (n - 2)):
        if i == d + k - 2:
            J.append(d)
        elif i == d + k - 1:
            J.append(k + d)
        else:
            J.append(i + k)
    J.append(d)
    J.append(d - 1 + k * (n - 1))

def check_conditions(k, J, A_round):
    d = k - 3
    n = (256 + k - 1 - d) // k
    Flag = False
    for i in range(n):
        if J[i] == A_round[i + 1]:
            Flag = True
        else:
            Flag = False
            break
    return Flag

def swap_elements(i, j, s_box):
    s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box

def MaxColStep(K, k, J):
    S = rc.init_s_box()
    j = 0
    for i in range(256):
        j = (j + S[i] + K[i % k]) % 256
        if check_conditions(k, J, store_j(k)) == False:
            return i
        else:
            S = swap_elements(i, j, S)
    return 255

def PassSecondRound(K1, k, A, J):
    d = k - 3
    p = MaxColStep(K1, k, J)
    while p < d + k:
        Q = MaxColStep(K1, k, J)
        if p % k == d - 2 or p % k == d - 1 or p % k == d or p % k == d + 1:
            return p
        for y in range(1, 256):
            K1 = K_xy_modif(K1, k, p % k, y)
            R = MaxColStep(K1, k, J)
            if R > Q:
                A[p % k] = y
                Q = R
            elif p > Q:
                return p
            else:
                K1 = K_xy_modif(K1, k, p % k, A[p % k])
            p = Q
    for y in range(1, 256):
        K1 = K_xy_modif(K1, k, p % k, y)
        p = MaxColStep(K1, k, J)
        if p > d + k:
            return p
    return 0

def K_xy_modif(K, k, c, v):
    K[c % k] = (K[c % k] + v) % 256
    K[(c + 1) % k] = (K[(c + 1) % k] - v) % 256
    return K

def Search(K1, k, A, J):
    d = k - 3
    p = MaxColStep(K1, k, J)
    if p == 255:
        return True
    Maxp = p
    Flag = False
    for x in range(0, d - 3):
        if A[x] == 0:
            for y in range(1, 256):
                K1 = K_xy_modif(K1, k, x, 1)
                T = MaxColStep(K1, k, J)
                if T == 255:
                    return True
                if T > Maxp:
                    Maxp = T
                    A[x] = y
                    Flag = True
        if Flag == True:
            K1 = K_xy_modif(K1, k, x, A[x])
            Flag = False
    if Maxp <= p:
        return False
    return Search(K1, k, A, J)

def K_xy(k, K1):
    d = k - 2
    for x in range(256): #x [0; 255]
        for y in range(1, 256, 1): #y [1; 255]
            if K1[x % k] != K1[d] or K1[x % k] != K1[d + 1]:
                K1[x % k] = (K1[x % k] + y) % 256
                K1[(x + 1) % k] = (K1[(x + 1) % k] - y) % 256
    return K1

def collision_search(J, k):
    d = k - 3
    n = (256 + k - 1 - d) // k
    K1 = generate_bytes_sequence(k, d)
    K2 = K1.copy()
    K1[d - 1] = (n - 1) * k - d - 2
    K1[d + 1] = k - d - 1
    print(bytes(K1), '\n', bytes(K2))
    T = MaxColStep(K1, k, J)
    while T < d - 2:
        T1 = MaxColStep(K1, k, J)
        for y in range(1, 256):
            K1 = K_xy_modif(K1, k, y, 1)
            T = MaxColStep(K1, k, J)
            if T > T1:
                break
        T = T1
    K1[d] = 256 - J[d - 1]
    A = []
    for i in range(k - 1):
        A[i] = 0
    T = PassSecondRound(K1, k, A)
    if T > d + k:
        if Search(K1, k, A, J) == True:
            return K1, K2