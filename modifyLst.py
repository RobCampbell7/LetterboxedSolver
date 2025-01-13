import re

def bannedCombinations(word):
    if re.search("[a-z]*[cj, cv, cx, dx, fq, fx, gq, gx, hx, jc, jf, jg, jq, js, jv, jw, jx, jz, kq, kx, mx, px, pz, qb, qc, qd, qf, qg, qh, qj, qk, ql, qm, qn, qp, qs, qt, qv, qw, qx, qy, qz, sx, vb, vf, vh, vj, vm, vp, vq, vt, vw, vx, wx, xj, xx, zj, zq, zx][a-z]*", word) == None:
        return True
    else:
        return False

def doubleLetter(word):
    for i in range(1, len(word)):
        if word[i] == word[i - 1]:
            return True
    return False

def allow(word):
    return len(word) > 3 and word.isalpha() and word.lower() == word #and bannedCombinations(word) == False

words = []
with open("wordsFromUnix.txt", "r") as dictFile:
    for li in dictFile.readlines():
        words.append(li.replace("\n", "").replace(" ", ""))

words.sort()
with open("words.txt", "w") as dictFile:
    for word in words:
        if allow(word) == True:
            dictFile.write(word.lower() + "\n")