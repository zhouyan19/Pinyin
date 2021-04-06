import os
import sys

sname = '../input/input_hz.txt'
scores = ''

def calculate(f, std):
    global scores
    num = len(std)
    cnt = 0
    acc = 0
    with open(f, 'r', encoding='utf-8') as test:
        sentences = test.readlines()
        for i in range(num):
            try:
                sentence = sentences[i].strip('\n').split()
                standard = std[i].strip('\n')
                if standard in sentence:
                    cnt += 1
            except Exception as e:
                print('Exception!', e, 'i =', i)
        acc = cnt / num
    info = "{:<40}{:>30}".format(f + " :", "acc:" + str(acc * 100) + '%')
    print(info)
    scores += info
    scores += '\n'


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        sname = sys.argv[1]
    try:
        with open(sname, 'r', encoding='utf-8') as s:
            std = s.readlines()
            for root,dirs,files in os.walk(r'..\result'):
                for file in files:
                    file = os.path.join(root, file)
                    calculate(file, std)
        with open('scores.txt', 'w+', encoding='utf-8') as fout:
            fout.write(scores)
        print('Done.')
    except Exception as e:
        print('Error!', e)