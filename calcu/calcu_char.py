import os
import sys

sname = '../input/input_hz.txt'
scores = ''

def calculate(f, std):
    global scores
    num = len(std)
    total = 0
    cnt = 0
    acc = 0
    with open(f, 'r', encoding='utf-8') as test:
        sentences = test.readlines()
        try:
            for i in range(num):
                sentence = sentences[i].strip('\n').split()[0]
                standard = std[i].strip('\n')
                total += len(standard)
                for j in range(len(sentence)):
                    if j >= len(standard) :
                        break
                    if standard[j] == sentence[j]:
                        cnt += 1
            acc = cnt / total
        except Exception as e:
            print('sentence:', sentence)
            print('Exception:', e)
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
        with open('scores_char.txt', 'w+', encoding='utf-8') as fout:
            fout.write(scores)
        print('Done.')
    except Exception as e:
        print('Error!', e)