#! usr/bin/python
# -*- coding: utf-8 -*-c
"""
将拼音进行分割
"""

all_list = ["a", "ai", "an", "ang", "ao", "ba", "bai", "ban", "bang", "bao",
            "bei", "ben", "beng", "bi", "bian", "biao", "bie", "bin", "bing",
            "bo", "bu", "ca", "cai", "can", "cang", "cao", "ce", "ceng", "cha",
            "chai", "chan", "chang", "chao", "che", "chen", "cheng", "chi",
            "chong", "chou", "chu", "chuai", "chuan", "chuang", "chui", "chun",
            "chuo", "ci", "cong", "cou", "cu", "cuan", "cui", "cun", "cuo",
            "da", "dai", "dan", "dang", "dao", "de", "deng", "di", "dian",
            "diao", "die", "ding", "diu", "dong", "dou", "du", "duan", "dui",
            "dun", "duo", "e", "en", "er", "fa", "fan", "fang", "fei", "fen",
            "feng", "fu", "fou", "ga", "gai", "gan", "gang", "gao", "ge",
            "ji", "gen", "geng", "gong", "gou", "gu", "gua", "guai", "guan",
            "guang", "gui", "gun", "guo", "ha", "hai", "han", "hang", "hao",
            "he", "hei", "hen", "heng", "hong", "hou", "hu", "hua", "huai",
            "huan", "huang", "hui", "hun", "huo", "jia", "jian", "jiang",
            "qiao", "jiao", "jie", "jin", "jing", "jiong", "jiu", "ju",
            "juan", "jue", "jun", "ka", "kai", "kan", "kang", "kao", "ke",
            "ken", "keng", "kong", "kou", "ku", "kua", "kuai", "kuan",
            "kuang", "kui", "kun", "kuo", "la", "lai", "lan", "lang", "lao",
            "le", "lei", "leng", "li", "lia", "lian", "liang", "liao",
            "lie", "lin", "ling", "liu", "long", "lou", "lu", "luan", "lue",
            "lun", "luo", "ma", "mai", "man", "mang", "mao", "me", "mei",
            "men", "meng", "mi", "mian", "miao", "mie", "min", "ming",
            "miu", "mo", "mou", "mu", "na", "nai", "nan", "nang", "nao",
            "ne", "nei", "nen", "neng", "ni", "nian", "niang", "niao", "nie",
            "nin", "ning", "niu", "nong", "nu", "nuan", "nue", "yao", "nuo",
            "o", "ou", "pa", "pai", "pan", "pang", "pao", "pei", "pen",
            "peng", "pi", "pian", "piao", "pie", "pin", "ping", "po", "pou",
            "pu", "qi", "qia", "qian", "qiang", "qie", "qin", "qing",
            "qiong", "qiu", "qu", "quan", "que", "qun", "ran", "rang",
            "rao", "re", "ren", "reng", "ri", "rong", "rou", "ru", "ruan",
            "rui", "run", "ruo", "sa", "sai", "san", "sang", "sao", "se",
            "sen", "seng", "sha", "shai", "shan", "shang", "shao", "she",
            "shen", "sheng", "shi", "shou", "shu", "shua", "shuai", "shuan",
            "shuang", "shui", "shun", "shuo", "si", "song", "sou", "su",
            "suan", "sui", "sun", "suo", "ta", "tai", "tan", "tang", "tao",
            "te", "teng", "ti", "tian", "tiao", "tie", "ting", "tong",
            "tou", "tu", "tuan", "tui", "tun", "tuo", "wa", "wai", "wan",
            "wang", "wei", "wen", "weng", "wo", "wu", "xi", "xia",
            "xian", "xiang", "xiao", "xie", "xin", "xing", "xiong", "xiu",
            "xu", "xuan", "xue", "xun", "ya", "yan", "yang", "ye", "yi",
            "yin", "ying", "yo", "yong", "you", "yu", "yuan", "yue", "yun",
            "za", "zai", "zan", "zang", "zao", "ze", "zei", "zen", "zeng",
            "zha", "zhai", "zhan", "zhang", "zhao", "zhe", "zhen", "zheng",
            "zhi", "zhong", "zhou", "zhu", "zhua", "zhuai", "zhuan",
            "zhuang", "zhui", "zhun", "zhuo", "zi", "zong", "zou", "zu",
            "zuan", "zui", "zun", "zuo", "jv", "qv", "xv", "lv", "nv"]


def segment(pylist):
    length = len(pylist)
    cur = 0
    res = []
    buf = ""
    match = ""
    greedy = False
    while True:
        if cur >= length:
            if buf != "":
                res.append(buf)
            break
        match += pylist[cur]
        if match in all_list:
            buf = match
            greedy = True
        elif greedy:
            if buf != "":
                res.append(buf)
            buf = ""
            match = match[-1]
            greedy = False
        cur += 1
    return res


if __name__ == "__main__":
    # while True:
    #     raw = input()
    #     res = segment(raw)
    #     print(res)
    fp = r"../input/"
    fp_in = fp + "no_space.txt"
    fp_std = fp + "input_py.txt"
    fp_out = fp + "拼音分割结果.txt"
    fin = open(fp_in, 'r', encoding="utf-8")
    fstd = open(fp_std, 'r', encoding="utf-8")
    fout = open(fp_out, 'w', encoding="utf-8")
    pys = fin.readlines()
    total = len(pys)
    cnt = 0
    for py in pys:
        res = segment(py)
        sentence = ""
        for w in res:
            sentence += w
            sentence += " "
        sentence = sentence.strip(" ")
        if sentence == fstd.readline().strip('\n'):
            cnt += 1
            fout.write("√ ")
        else:
            fout.write("× ")
        fout.write(sentence)
        fout.write('\n')
    acc = cnt / total
    info = "{:<12}{:<30}".format(
        "cnt:" + str(cnt), "accuracy:" + str(acc * 100) + '%')
    fout.write(info)
    print(info)
    fout.close()
    fstd.close()
    fin.close()
