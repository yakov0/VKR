import JPLib as jp

k = 32

d = k - 3

J = jp.store_j(k)

K1, K2 = jp.collision_search(J, k)

print(K1, K2)