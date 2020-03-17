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

def kmp_string_matching(text, pattern):
    pi = prefix_function(pattern)
    q = 0
    ans = 0
    for i in range(0, len(text)):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q-1]
        if pattern[q] == text[i]:
            q = q + 1
        if q == len(pattern):
            ans += i + 1 -q
            q = pi[q-1]

    return ans

def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k-1]
        if pattern[k] == pattern[q]:
            k = k + 1
        pi.append(k)
    return pi

@timer
def main_naive():
    ans = 0
    with open("kon.txt") as f:
        for line in load_chunk(f):
            ans += naive(line, "kruszwil")
    print(f"{ans}")

@timer
def main_fa():
    ans = 0
    alphabet = {chr(x) for x in range(0, 255) } | {'\n'}

    with open("kon.txt") as f:
        for line in load_chunk(f):
            ans += fa_string_matching(line, transition_table("kruszwil", alphabet))
    print(f"{ans}")

@timer
def main_kmp():
    ans = 0
    with open("kon.txt") as f:
        for line in load_chunk(f):
            ans += kmp_string_matching(line, "kruszwil")

    print(f"{ans}")

if __name__ == "__main__":
    main_naive()
    main_fa()
    main_kmp()


