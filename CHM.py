import CHMLib as ch

k = 32

d = k - 3

K1 = ch.generate_bytes_sequence(k, d)
print(K1)

K1, K2 = ch.first_modification(K1, k)
print(bytes(K1), '\n', bytes(K2))

K1, K2 = ch.run_ksa(k, K1, K2)
print(K1, K2)