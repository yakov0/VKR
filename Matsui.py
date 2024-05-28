import MatsuiLib as ml

k = 22

d = k - 1

K1, K2 = ml.generate_bytes_sequence(k, d)
print(K1,'\n', K2)

ml.first_modification(K1, K2, k, d)
print(K1, '\n', K2)
print(bytes(K1), '\n', bytes(K2))

R = ml.search(k, K1, K2)
print(R)

R = ml.find_keys(k, K1, K2)
print(R)
print(K1, '\n', K2)

# print(rc.init_s_box_rc4(R1))
# print(rc.init_s_box_rc4(R2))
