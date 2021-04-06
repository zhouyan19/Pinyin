#! usr/bin/python
# -*- coding: utf-8 -*-c
"""
STEP5: 拼音输入法，取n-best
"""
import json
import heapq
import sys

LAM = 0.999992
M_NUM = 5
fpath = r"../src/"

ppath = fpath + "pyhzb.txt"
pydic = {}  # 拼音-汉字列表的字典

pdpath = fpath + "no_seg_zhihu_pair_cnt.json"
cdpath = fpath + "zhihu_char_cnt.json"
pdic = {}  # 二元组字典
cdic = {}  # 汉字字典

total = 0

with open(ppath, 'r') as fp:
    entries = fp.readlines()
    for entry in entries:
        entry = entry.split()
        pydic[entry[0]] = entry[1:]

with open(pdpath, 'r', encoding='utf-8') as pd:
    pdic = json.load(pd)

with open(cdpath, 'r', encoding='utf-8') as cd:
    cdic = json.load(cd)

total = len(cdic.keys())


def pro(now):
    if int(cdic[now]) == 0:
        return 0
    return float(cdic[now]) / total


def post_pro(now, pre=""):
    if pre != "":
        if pre+now in pdic:
            pn = float(pdic[pre+now])
            p = float(cdic[pre])
            return LAM * (pn/p) + (1-LAM) * pro(now)
        else:
            return (1-LAM) * pro(now)
    return pro(now)


def calcu(score, now, pre=""):
    score *= post_pro(now, pre)
    return score


def this_max(pre_scores, ch, pre_py):
    pre_s = []
    for l in pre_scores:
        pre_s += l
    scores = []
    ids = []
    max_c = []
    num = len(pre_s)
    if num == len(pre_scores):
        for i in range(num):
            pre = pydic[pre_py][i]
            s = calcu(pre_s[i], ch, pre)
            scores.append(s)
        max_s = heapq.nlargest(M_NUM, scores)
        for s in max_s:
            idx = scores.index(s)
            idab = (idx, 0)
            ids.append(idab)
            max_c.append(pydic[pre_py][idx])
    else:
        for i in range(num):
            pre = pydic[pre_py][i//M_NUM]
            s = calcu(pre_s[i], ch, pre)
            scores.append(s)
        max_s = heapq.nlargest(M_NUM, scores)
        for s in max_s:
            idx = scores.index(s)
            ida = idx // M_NUM
            idb = idx % M_NUM
            idab = (ida, idb)
            ids.append(idab)
            max_c.append(pydic[pre_py][ida])
    return max_s, ids, max_c


def viterbi(pylist):
    sentences = []
    scores = []
    for py in pylist:
        num = len(pydic[py])
        scores.append([[0.0 for j in range(M_NUM)] for i in range(num)])
        sentences.append([["" for j in range(M_NUM)] for i in range(num)])
    for j in range(len(scores[0])):
        scores[0][j] = [calcu(1.0, pydic[pylist[0]][j])]
    for i in range(1, len(scores)):
        py = pylist[i]
        for j in range(len(scores[i])):
            ch = pydic[py][j]
            scores[i][j], ids, max_c = this_max(scores[i-1], ch, pylist[i-1])
            for k in range(len(ids)):
                ida = ids[k][0]
                idb = ids[k][1]
                sentences[i][j][k] = sentences[i-1][ida][idb] + max_c[k]
            # print("scores:", scores[i][j])
            # print("sentences:", sentences[i][j])
    final_scores = []
    for l in scores[-1]:
        final_scores += l
    max_s = heapq.nlargest(M_NUM, final_scores)
    # print("max_s:", max_s)
    res = []
    for s in max_s:
        idm = final_scores.index(s)
        ida = idm // M_NUM
        idb = idm % M_NUM
        max_r = sentences[-1][ida][idb] + pydic[pylist[-1]][ida]
        res.append(max_r)
    return res


if __name__ == "__main__":
    # while True:
    #     raw = input()
    #     pinyin = raw.split()
    #     res = viterbi(pinyin)
    #     print(res)

    in_name = "../input/input_py.txt"
    out_name = "../result/zhihu_nbest_" + str(LAM) + ".txt"

    if len(sys.argv) >= 2:
        in_name = sys.argv[1]
    if len(sys.argv) >= 3:
        out_name = sys.argv[2]
    fp_in = in_name
    fp_out = out_name

    fin = open(fp_in, 'r', encoding="utf-8")
    fout = open(fp_out, 'w', encoding="utf-8")

    pys = fin.readlines()

    for py in pys:
        py = py.split()
        res = viterbi(py)
        for sentence in res:
            fout.write(sentence + " ")
        fout.write('\n')

    fout.close()
    fin.close()
