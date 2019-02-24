c1 = [3, 2, 5, 3, 2, 4]
c2 = []
for i, x in enumerate(c1):
    if i == 0:
        p = 0
    else:
        p = c1[i - 1]
    if i == len(c1) - 1:
        n = 0
    else:
        n = c1[i + 1]

    if x > p:
        if x > n:
            c2_v = 0
        elif x < n:
            c2_v = 2
        else:
            c2_v = 'not_defined'
    elif x < p:
        if x > n:
            c2_v = 3
        elif x < n:
            c2_v = 1
        else:
            c2_v = 'not_defined'
    else:
        c2_v = 'not_defined'
    c2.append(c2_v)
print(c2)
