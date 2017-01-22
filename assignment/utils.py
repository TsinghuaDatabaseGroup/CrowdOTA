from math import log
def entropy(drb):
    eps = 1e-7
    ans = 0
    for x in drb:
        ans = ans - x * log(x+eps)
    return ans