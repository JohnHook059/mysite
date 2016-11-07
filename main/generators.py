import random

def invite_generator():
    random.seed()
    l = []
    for i in range(10):
        l.append(chr(ord('0') + i))
    for i in range(26):
        l.append(chr(ord('a') + i))
        l.append(chr(ord('A') + i))

    ans = ''
    for i in range(7):
        for j in range(5):
            ans += random.choice(l)
        ans += '-'
    return ans[:-1]
