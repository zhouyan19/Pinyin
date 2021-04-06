#! usr/bin/python
# -*- coding: utf-8 -*-c
"""
STEP5: 拼音输入法,基础功能,语料处理中经过分词
"""
import json
import sys

lam = 0.99999

fpath = r"../src/"

ppath = fpath + "pyhzb.txt"
pydic = {}  # 拼音-汉字列表的字典

pdpath = fpath + "sina_pair_cnt.json"
cdpath = fpath + "sina_char_cnt.json"
pdic = {}  # 二元组字典
cdic = {}  # 汉字字典

total = 0

with open(ppath, 'r') as fp:
    entries = fp.readlines()
    for entry in entries:
        entry = entry.split()
        pydic[entry[0]] = entry[1:]

with open(pdpath, 'r') as pd:
    pdic = json.load(pd)

with open(cdpath, 'r') as cd:
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
            return lam * (pn/p) + (1-lam) * pro(now)
        else:
            return (1-lam) * pro(now)
    return pro(now)


def calcu(score, now, pre=""):
    score *= post_pro(now, pre)
    return score


def this_max(pre_scores, ch, pre_py):
    scores = []
    num = len(pre_scores)
    for i in range(num):
        pre = pydic[pre_py][i]
        s = calcu(pre_scores[i], ch, pre)
        scores.append(s)
    max_s = max(scores)
    idx = scores.index(max_s)
    max_c = pydic[pre_py][idx]
    return max_s, idx, max_c


def viterbi(pylist):
    sentences = []
    scores = []
    for py in pylist:
        num = len(pydic[py])
        scores.append([0.0 for i in range(num)])
        sentences.append(["" for i in range(num)])
    for j in range(len(scores[0])):
        scores[0][j] = calcu(1.0, pydic[pylist[0]][j])
    for i in range(1, len(scores)):
        py = pylist[i]
        for j in range(len(scores[i])):
            ch = pydic[py][j]
            scores[i][j], idx, max_c = this_max(scores[i-1], ch, pylist[i-1])
            sentences[i][j] = sentences[i-1][idx] + max_c
        # print(scores)
        # print(sentences)
    max_s = max(scores[-1])
    idm = scores[-1].index(max_s)
    res = sentences[-1][idm] + pydic[pylist[-1]][idm]
    return max_s, res


if __name__ == "__main__":
    # while True:
    #     raw = input()
    #     pinyin = raw.split()
    #     max_s, res = viterbi(pinyin)
    #     print(res)

    in_name = "../input/input_py.txt"
    out_name = "../result/sina_jieba_" + str(lam) + ".txt"

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
        max_s, res = viterbi(py)
        fout.write(res + '\n')

    print("Done.")
    fout.close()
    fin.close()
