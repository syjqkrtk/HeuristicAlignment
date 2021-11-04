import matplotlib.pyplot as plt
import numpy as np
import time
import random

l_seqs = 1000
n_actions = 3      # number of actions {match123, match12, match23, match31, gap1, gap2, gap3} : {(x+1,y+1,z+1), (x+1,y+1,z), (x,y+1,z+1), (x+1,y,z+1), (x+1,y,z), (x,y+1,z), (x,y,z+1)}
n_episodes = 1   # number of episodes to run
reward = [1,-1,-1]    # reward for each (match, gap, mismatch)
#Ecoli1 = open("Hepatitis_1.txt",'r')
#Ecoli2 = open("Hepatitis_2.txt",'r')
#Ecoli3 = open("Hepatitis_3.txt",'r')
Ecoli1 = open("Ecoli_1.txt",'r')
Ecoli2 = open("Ecoli_2.txt",'r')
#Ecoli1 = open("MT_1.txt",'r')
#Ecoli2 = open("MT_2.txt",'r')
#Ecoli3 = open("MT_3.txt",'r')

ecoli1 = list(Ecoli1.readline())
test1 = np.zeros(np.size(ecoli1)-1)
for _ in range(np.size(ecoli1)-1):
    test1[_] = (ecoli1[_]=='A')+2*(ecoli1[_]=='C')+3*(ecoli1[_]=='G')+4*(ecoli1[_]=='T')-1

'''
print(test1)
while ecoli1:
    ecoli1 = list(Ecoli1.readline())
    for _ in range(np.size(ecoli1)-1):
        temp1 = np.zeros(np.size(ecoli1)-1)
        temp1[_] = (ecoli1[_]=='A')+2*(ecoli1[_]=='C')+3*(ecoli1[_]=='G')+4*(ecoli1[_]=='T')-1
    print(temp1)
    test1 = np.append(test1,temp1)
'''

ecoli2 = list(Ecoli2.readline())
test2 = np.zeros(np.size(ecoli2)-1)
for _ in range(np.size(ecoli2)-1):
    test2[_] = (ecoli2[_]=='A')+2*(ecoli2[_]=='C')+3*(ecoli2[_]=='G')+4*(ecoli2[_]=='T')-1

'''
ecoli3 = list(Ecoli3.readline())
test3 = np.zeros(np.size(ecoli3)-1)
for _ in range(np.size(ecoli3)-1):
    test3[_] = (ecoli3[_]=='A')+2*(ecoli3[_]=='C')+3*(ecoli3[_]=='G')+4*(ecoli3[_]=='T')-1
'''

Ecoli1.close()
Ecoli2.close()
#Ecoli3.close()
#print(test1, test2, test3)
test1 = test1.astype(int)
test2 = test2.astype(int)
#test3 = test3.astype(int)

def zipfian(s, N):
    temp0 = np.array(range(1, N + 1))
    temp0 = np.sum(1 / temp0 ** s)
    temp = random.random() * temp0

    for i in range(N):
        temp2 = 1 / ((i + 1) ** s)

        if temp < temp2:
            return i + 1
        else:
            temp = temp - temp2

    return 0


def rewardfun(s1, s2, a):
    result = 0
    if s1 == s2 and a == 0:
        result = result + reward[0]
    elif s1 != s2 and a == 0:
        result = result + reward[2]
    else:
        result = result + reward[1]

    return result


'''
def rewardfun(s1, s2, s3, a):
    result = 0
    if s1 == s2 and (a == 0 or a == 1):
        result = result + reward[0]
    elif s1 != s2 and (a == 0 or a == 1):
        result = result + reward[2]
    elif a != 6:
        result = result + reward[1]
    else:
        result = result

    if s2 == s3 and (a == 0 or a == 2):
        result = result + reward[0]
    elif s2 != s3 and (a == 0 or a == 2):
        result = result + reward[2]
    elif a != 4:
        result = result + reward[1]
    else:
        result = result

    if s3 == s1 and (a == 0 or a == 3):
        result = result + reward[0]
    elif s3 != s1 and (a == 0 or a == 3):
        result = result + reward[2]
    elif a != 5:
        result = result + reward[1]
    else:
        result = result

    return result
'''


def seqgen(l_seqs, n_length):
    seq1 = np.random.randint(4, size=l_seqs)
    seq2 = np.mod(seq1 + (np.random.rand(l_seqs) < 0.1) * np.random.randint(4, size=l_seqs), 4)
    count1 = 0
    count2 = 0
    for kk in range(l_seqs):
        if np.random.rand() < 0.05:
            indel = zipfian(1.6, 3)
            ranval = np.random.rand()
            if ranval < 1 / 2:
                temp1 = seq1[0:kk + count1]
                temp4 = seq1[kk + count1:]
                seq1 = np.append(np.append(temp1, np.random.randint(4, size=indel)), temp4)
                count1 = count1 + 1
            else:
                temp2 = seq2[0:kk + count2]
                temp5 = seq2[kk + count2:]
                seq2 = np.append(np.append(temp2, np.random.randint(4, size=indel)), temp5)
                count2 = count2 + 1
                '''
            else:
                temp3 = seq3[0:kk+count3]
                temp6 = seq3[kk+count3:]
                seq3 = np.append(np.append(temp3,np.random.randint(4, size=indel)),temp6)
                count3 = count3 + 1
                '''

    extendseq = np.zeros(n_length - 1, dtype=int) - 1
    seq1 = np.append(seq1, extendseq)
    seq2 = np.append(seq2, extendseq)

    return seq1, seq2


def shortalign(s1, s2):
    n_length = np.size(s1)
    score = np.zeros([n_length + 1, n_length + 1], dtype=int)
    pathx = np.zeros([n_length, n_length], dtype=int)
    pathy = np.zeros([n_length, n_length], dtype=int)
    score[0, :] = range(0, -2 * n_length - 2, -2)
    score[:, 0] = range(0, -2 * n_length - 2, -2)

    for i in range(1, n_length + 1):
        for j in range(1, n_length + 1):
            temp = [score[i - 1, j - 1] + rewardfun(s1[i - 1], s2[j - 1], 0),
                    score[i - 1, j] + rewardfun(s1[i - 1], s2[j - 1], 1),
                    score[i, j - 1] + rewardfun(s1[i - 1], s2[j - 1], 2)]
            temp2 = max(temp)
            score[i, j] = temp2
            temp3 = temp.index(temp2)
            if temp3 == 0:
                pathx[i - 1, j - 1] = i - 2
                pathy[i - 1, j - 1] = j - 2
            elif temp3 == 1:
                pathx[i - 1, j - 1] = i - 2
                pathy[i - 1, j - 1] = j - 1
            else:
                pathx[i - 1, j - 1] = i - 1
                pathy[i - 1, j - 1] = j - 2

    x = n_length - 1
    y = n_length - 1

    while x >= 0 and y >= 0:
        tempx = pathx[x, y]
        tempy = pathy[x, y]
        x = tempx
        y = tempy

    if x == y:
        return 0, rewardfun(s1[0], s2[0], 0)
    elif x > y:
        return 1, rewardfun(s1[0], s2[0], 1)
    else:
        return 2, rewardfun(s1[0], s2[0], 2)


def alignment(n_length, n_episodes, seq1, seq2):
    for k in range(n_episodes):
        # seq1, seq2 = seqgen(l_seqs,n_length)
        # l_seq1 = np.size(seq1) - n_length + 1
        # l_seq2 = np.size(seq2) - n_length + 1
        extendseq = np.zeros(n_length - 1, dtype=int) - 1
        seq1 = np.append(seq1, extendseq)
        seq2 = np.append(seq2, extendseq)
        l_seq1 = np.size(seq1) - n_length + 1
        l_seq2 = np.size(seq2) - n_length + 1
        s1 = seq1[0:n_length]
        s2 = seq2[0:n_length]
        x, y = 0, 0
        score = 0
        while x < l_seq1 and y < l_seq2:
            a, s = shortalign(s1, s2)
            score = score + s
            if a == 0:
                x, y = x + 1, y + 1
            elif a == 1:
                x, y = x + 1, y
            else:
                x, y = x, y + 1

            s1 = seq1[x:x + n_length]
            s2 = seq2[y:y + n_length]
        print('score : ' + str(score))
        file.write(str(score) + '\n')

    return 0


#n_length = 30                    # 염기서열 몇개씩 볼지 parameter (x,y)
for n_length in [1,2,3,5,10,20,30,50,100,200,300,500,1000]:
    file = open("result"+str(n_length)+".txt", "w")
    past = time.time()
    print('-------------')
    print("win   : "+str(n_length))
    alignment(n_length, n_episodes, ecoli1, ecoli2)
    #alignment(n_length, n_episodes, ecoli1, ecoli3)
    now = time.time()
    print("time  : "+str(now-past))
    file.write(str(now-past) + '\n')
    '''
    for i in range(1,100):
        seq1 = np.random.randint(4, size=l_seqs)
        # seq2 = seq1
        # seq2 = np.random.randint(4, size=l_seqs)
        seq2 = np.mod(seq1 + (np.random.rand(l_seqs) < 0.1) * np.random.randint(4, size=l_seqs), 4)
        count1 = 0
        count2 = 0
        # count3 = 0

        for kk in range(l_seqs):
            if np.random.rand() < 0.02:
                indel = zipfian(1.6, 1)
                ranval = np.random.rand()
                if ranval < 1 / 2:
                    temp1 = seq1[0:kk + count1]
                    temp4 = seq1[kk + count1:]
                    seq1 = np.append(np.append(temp1, np.random.randint(4, size=indel)), temp4)
                    count1 = count1 + 1
                else:
                    temp2 = seq2[0:kk + count2]
                    temp5 = seq2[kk + count2:]
                    seq2 = np.append(np.append(temp2, np.random.randint(4, size=indel)), temp5)
                    count2 = count2 + 1

        alignment(n_length, n_episodes, seq1, seq2)
    '''
    file.close()