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
    # print(J)
    # print(J[2])

#store_j(22)

def first_modification(K1, k):
    d = k - 3
    n = (256 + k - 1 - d)//k
    K1[d - 1] = (n - 1) * k - d - 2
    K1[d + 1] = k - d - 1
    K2 = K1.copy()
    K2[d] = K1[d] + 1
    return K1, K2

def find_sum(K, S, k):
    J = store_j(k)
    K = K[0:k - 2]
    S = S[k - 1: 2 * k - 2]
    sum_v = J[2] - J[1] - sum(K) - sum(S)
    return sum_v

def round(K1, K2, k):
    d = k - 3
    n = (256 + k - 1 - d) // k
    count = 0
    for t in range(n):
        if K1[d + (t - 1) * k] == d + t * k:
            count += 1
    return count

def modify_key(dr, r, K, J):
    K[dr] = K[dr] + r - J[0]
    K[dr + 1] = K[dr + 1] - r - J[0]
    return K

def newsearch(K1, K2, S1, J, k, R):
    d = k - 3
    n = (256 + k - 1 - d) // k
    if round(K1,K2) == n:
        return n
    MaxR = round(K1, K2)
    t = round(K1, K2) + 1
    r = (t - 1) * k + d
    while r > (t - 2) * k + d:
        del_r = (k - sum(K1[0:k]) - sum(S1[r-k+1:r-1])) % 256
        if del_r <= (t - 2) * k + d:
            K1 = modify_key(del_r, r, K1, J)
            K2 = modify_key(del_r, r, K2, J)
        if round(K1, K2) <= MaxR or R == n:
            return round(K1, K2)
        else:
            R += 1
            newsearch(K1, K2, S1, J, k, R)
        r -= 1
    return 0

def run_ksa(k, K1, K2):
    J = store_j(k)
    d = k - 3
    n = (256 + k - 1 - d) // k
    S1 = rc.init_s_box()
    S2 = rc.init_s_box()
    j = 0
    for i in range(256):
        j = (j + S1[i] + K1[i % len(K1)]) % 256
        S1[i], S1[j] = S1[j], S1[i]
        j = (j + S2[i] + K2[i % len(K2)]) % 256
        S2[i], S2[j] = S2[j], S2[i]
        if i == d - 1:
            K1[d] = 256 - j
            K2[d] = K1[d] + 1
        if i == d + 1:
            K1[d + 2] = find_sum(K1, S1, k)
            K2[d + 2] = find_sum(K2, S2, k)
    R = 0
    if newsearch(K1, K2, S1, J, k, R) == n:
        return K1, K2
    else:
        run_ksa(k, K1, K2)



