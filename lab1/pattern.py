"""
Pattern matching
"""
from time import time
import re

def load_chunk(f):
    while True:
        data = f.readline()
        if not data:
            break
        yield data

def timer(func):
    def wrapper(*args):
        start = time()
        S =  func(*args)
        stop = time()-start
        print(f"time {stop}")
        return S
    return wrapper

def naive(text, pattern):
    S = set()
    for s in range(len(text)-len(pattern)+1):
        if pattern == text[s:s+len(pattern)]:
            S.add(s)
    return len(S)

def fa_string_matching(text, delta):
    q = 0
    ans = 0
    for s in range(0, len(text)):
        q = delta[q][text[s]]
        if(q == len(delta) - 1):
           ans += s+1-q
    return ans

def transition_table(pattern, alphabet):
    result = []
    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in alphabet:
            k = min(len(pattern) + 1, q + 2)
            while True:
                k = k - 1
                if(re.search(f"{pattern[:k]}$", pattern[:q] + a)):
                    break
            result[q][a] = k
    return result

@timer
def main_naive():
    ans = 0
    with open("konst.txt") as f:
        for line in load_chunk(f):
            ans += naive(line, "art")
    print(f"{ans}")

@timer
def main_fa():
    ans = 0
    alphabet = {chr(x) for x in range(32, 127) } | {'\n'}

    with open("konst.txt") as f:
        for line in load_chunk(f):
            ans += fa_string_matching(line, transition_table("art", alphabet))
    print(f"{ans}")

if __name__ == "__main__":
    main_naive()
    main_fa()


