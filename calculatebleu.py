import sys, os
from os import listdir
from os.path import isfile, join
from math import exp, log
from collections import Counter
def main():
    file1 = open(sys.argv[1], "r")
    reference_path = sys.argv[2]
    files =[]
    files.append(file1)
    if os.path.isdir(reference_path):
        temp_files = os.listdir(reference_path)
        temp_files = [ reference_path+"/"+file for file in temp_files]
        for file in temp_files:
            files.append(open(file,"r"))
        # files = files + temp_files
    else:
        files.append(open(reference_path,"r"))

    ngram_r = []
    references = []
    ngram_c = []
    ngram = {}
    z = 0
    t_total = 0
    precision = {}
    references_len = []
    candidates_len = []
    sentences = []
    for j in range(1, 5):
        ngram[j] = {}
    for line in files[0]:
        # if i==0:
        candidate = line.split()
        candidate = [c.lower() for c in candidate]
        length_candidates = len(candidate)
        candidates_len.append(length_candidates)
        ngram[1] = dict(Counter(candidate).most_common())
        ngram[2] = dict(Counter([' '.join(candidate[i:i + 2]) for i in range(len(candidate) - 1)]).most_common())
        ngram[3] = dict(Counter([' '.join(candidate[i:i + 3]) for i in range(len(candidate) - 2)]).most_common())
        ngram[4] = dict(Counter([' '.join(candidate[i:i + 4]) for i in range(len(candidate) - 3)]).most_common())
        ngram_c.append(dict(ngram))
        # print(ngram_c)
        for i in range(1, len(files)):
            line1 = files[i].readline()
            # length_temp = []
            tempngram = {}
            ngram_temp = []
            for j in range(1, 5):
                tempngram[j] = {}
            ref_temp = line1.split()
            ref_temp = [r.lower() for r in ref_temp]
            length_temp = len(ref_temp)
            tempngram[1] = dict(Counter(ref_temp).most_common())
            tempngram[2] = dict(Counter([' '.join(ref_temp[i:i + 2]) for i in range(len(ref_temp) - 1)]).most_common())
            tempngram[3] = dict(Counter([' '.join(ref_temp[i:i + 3]) for i in range(len(ref_temp) - 2)]).most_common())
            tempngram[4] = dict(Counter([' '.join(ref_temp[i:i + 4]) for i in range(len(ref_temp) - 3)]).most_common())
            ngram_temp.append(dict(tempngram))
            # print(ngram_temp[0][1])
            if references:
                ngram_r[0][1].update(
                    {k: max(ngram_r[0][1].get(k, -1), ngram_temp[0][1][k]) for k in ngram_temp[0][1]})
                ngram_r[0][2].update(
                    {k: max(ngram_r[0][2].get(k, -1), ngram_temp[0][2][k]) for k in ngram_temp[0][2]})
                ngram_r[0][3].update(
                    {k: max(ngram_r[0][3].get(k, -1), ngram_temp[0][3][k]) for k in ngram_temp[0][3]})
                ngram_r[0][4].update(
                    {k: max(ngram_r[0][4].get(k, -1), ngram_temp[0][4][k]) for k in ngram_temp[0][4]})
                if abs(length_temp - length_candidates) < abs(length_references - length_candidates):
                    length_references = length_temp
                else:
                    length_references
            else:
                references = ref_temp
                ngram_r = ngram_temp
                length_references = length_temp
        references_len.append(length_references)

        # one=ngram_c[0][1].values()
        # two=ngram_c[0][2].values()
        precision[line] = {}
        for m in range(1, 5):
            precision[line][m] = []
            total = sum(ngram_c[z][m].values())
            num = 0.0
            for x in ngram_c[z][m]:
                if x in ngram_r[0][m]:
                    num1 = ngram_c[z][m][x]
                    num2 = ngram_r[0][m][x]
                    num += min(ngram_c[z][m][x], ngram_r[0][m][x])
                else:
                    num += 0
            precision[line][m].append(num)
            precision[line][m].append(total)
        z += 1
        sentences.append(line)

    p1, p2, p3, p4 = 0, 0, 0, 0
    p1_num, p1_den, p2_num, p2_den, p3_num, p3_den, p4_num, p4_den = 0, 0, 0, 0, 0, 0, 0, 0
    for s in precision.keys():
        p1_num += precision[s][1][0]
        p1_den += precision[s][1][1]
        p2_num += precision[s][2][0]
        p2_den += precision[s][2][1]
        p3_num += precision[s][3][0]
        p3_den += precision[s][3][1]
        p4_num += precision[s][4][0]
        p4_den += precision[s][4][1]

    p1 = p1_num / p1_den
    p2 = p2_num / p2_den
    p3 = p3_num / p3_den
    p4 = p4_num / p4_den
    r = sum(references_len)
    c = sum(candidates_len)

    if c > r:
        bp = 1
    else:
        bp = exp(1 - (float(r) / c))

    gm = exp((0.25 * log(p1)) + (0.25 * log(p2)) + (0.25 * log(p3)) + (0.25 * log(p4)))

    bleu = bp * gm
    print(bleu)
    f1 = open('bleu_out.txt', 'w')
    f1.write(str(bleu))
    f1.close()


main()