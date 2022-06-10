#!/usr/bin/python3
from collections import Counter
import matplotlib.pyplot as plt
import random
import requests
import timeit

ADDR="172.43.2.6"
PORT=4000

CODES = Counter()
CODES2 = []

PHONES = ['IP12', 'IP13P', 'REA5', 'REAX2']

def get():
    r = requests.get("http://{}:{}".format(ADDR, PORT))
    CODES[r.status_code] += 1
    CODES2.append(r.status_code)

def post():
    r = requests.post("http://{}:{}/add".format(ADDR, PORT), data={'quantity': 1, 'code': random.choice(PHONES)})
    CODES[r.status_code] += 1
    CODES2.append(r.status_code)

def static():
    r = requests.get("http://{}:{}/static/images/Iphone_13Pro.jpeg".format(ADDR, PORT))
    CODES[r.status_code] += 1
    CODES2.append(r.status_code)

REPEAT=10000
res = timeit.repeat(post, repeat=REPEAT, number=1)
print('Total time:', sum(res))
print('Mean time:', sum(res)/REPEAT)
print(CODES)

plt.scatter(range(REPEAT), res, s=1, color=list(map(lambda x: [0, 1, 0] if x == 200 else [1, 0, 0], CODES2)))
plt.ylabel('Total time')
plt.show()
