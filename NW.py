import matplotlib.pyplot as plt
import numpy as np
import time
import random

n_length = 200       # 염기서열 몇개씩 볼지 parameter (x,y)
n_states = [n_length, n_length, n_length] # 총 state의 가짓수
n_actions = 3      # number of actions {match123, match12, match23, match31, gap1, gap2, gap3} : {(x+1,y+1,z+1), (x+1,y+1,z), (x,y+1,z+1), (x+1,y,z+1), (x+1,y,z), (x,y+1,z), (x,y,z+1)}
n_episodes = 1   # number of episodes to run
l_seqs = 1000
l_seqs2 = 1000
reward = [1,-1,-1]    # reward for each (match, gap, mismatch)
file = open("result.txt", "w")
Ecoli1 = open("Hepatitis_1.txt",'r')
Ecoli2 = open("Hepatitis_2.txt",'r')
Ecoli3 = open("Hepatitis_3.txt",'r')
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

ecoli3 = list(Ecoli3.readline())
test3 = np.zeros(np.size(ecoli3)-1)
for _ in range(np.size(ecoli3)-1):
    test3[_] = (ecoli3[_]=='A')+2*(ecoli3[_]=='C')+3*(ecoli3[_]=='G')+4*(ecoli3[_]=='T')-1

Ecoli1.close()
Ecoli2.close()
Ecoli3.close()
print(test1, test2, test3)
test1 = test1.astype(int)
test2 = test2.astype(int)
test3 = test3.astype(int)

def zipfian(s,N):
    temp0 = np.array(range(1,N+1))
    temp0 = np.sum(1/temp0**s)
    temp = random.random() * temp0

    for i in range(N):
        temp2 = 1 / ((i + 1) ** s)

        if temp < temp2:
            return i+1
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

def seqgen(l_seqs,n_length):
    seq1 = np.random.randint(4, size=l_seqs)
    seq2 = np.mod(seq1 + (np.random.rand(l_seqs)  < 0.1)*np.random.randint(4, size=l_seqs),4)
    count1 = 0
    count2 = 0
    for kk in range(l_seqs):
        if np.random.rand() < 0.05:
            indel = zipfian(1.6,3)
            ranval = np.random.rand()
            if ranval < 1/2:
                temp1 = seq1[0:kk+count1]
                temp4 = seq1[kk+count1:]
                seq1 = np.append(np.append(temp1,np.random.randint(4, size=indel)),temp4)
                count1 = count1 + 1
            else:
                temp2 = seq2[0:kk+count2]
                temp5 = seq2[kk+count2:]
                seq2 = np.append(np.append(temp2,np.random.randint(4, size=indel)),temp5)
                count2 = count2 + 1
                '''
            else:
                temp3 = seq3[0:kk+count3]
                temp6 = seq3[kk+count3:]
                seq3 = np.append(np.append(temp3,np.random.randint(4, size=indel)),temp6)
                count3 = count3 + 1
                '''

    extendseq = np.zeros(n_length - 1, dtype=int)-1
    seq1 = np.append(seq1, extendseq)
    seq2 = np.append(seq2, extendseq)

    return seq1, seq2

def shortalign(s1, s2):
    x_length = n_length
    y_length = n_length
    score = np.zeros([x_length+1,y_length+1], dtype=int)
    pathx = np.zeros([x_length,y_length], dtype=int)
    pathy = np.zeros([x_length,y_length], dtype=int)
    score[0,:] = range(0,-y_length-1,-1)
    score[:,0] = range(0,-x_length-1,-1)

    file3 = open("path2.txt","w")
    for i in range(1,x_length):
        for j in range(1,y_length):
            temp = [score[i-1,j-1]+rewardfun(s1[i-1],s2[j-1],0),score[i-1,j]+rewardfun(s1[i-1],s2[j-1],1),score[i,j-1]+rewardfun(s1[i-1],s2[j-1],2)]
            temp2 = max(temp)
            score[i, j] = temp2
            temp3 = temp.index(temp2)
            if temp3 == 0:
                pathx[i-1,j-1] = i-2
                pathy[i-1,j-1] = j-2
            elif temp3 == 1:
                pathx[i-1,j-1] = i-2
                pathy[i-1,j-1] = j-1
            else:
                pathx[i-1,j-1] = i-1
                pathy[i-1,j-1] = j-2
            file3.write(str([pathx[i-1,j-1],pathy[i-1,j-1]])+" "+"\t")
            file3.write(str(score[i,j])+" "+"\t")
        file3.write("\n")
    file3.close()

    #print(score[-2,:],score[:,-2])
    file4 = open("align2.txt","w")
    x = x_length-1
    y = y_length-1
    while x > 0 and y > 0:
        file4.write(str([x,y])+" "+str(score[x+1,y+1]))
        file4.write("\n")
        xp = pathx[x,y]
        yp = pathy[x,y]
        x = xp
        y = yp
    file4.write(str([x,y])+" "+str(score[x+1,y+1]))
    file4.write("\n")
    file4.close()

    #print(score[-2,:],score[:,-2])
    return max(np.max(score[-2,:]),np.max(score[:,-2]))

def align(s1, s2):
    x_length = np.size(s1)
    y_length = np.size(s2)
    score = np.zeros([x_length+1,y_length+1], dtype=int)
    pathx = np.zeros([x_length,y_length], dtype=int)
    pathy = np.zeros([x_length,y_length], dtype=int)
    score[0,:] = range(0,-y_length-1,-1)
    score[:,0] = range(0,-x_length-1,-1)

    file3 = open("path.txt","w")
    for i in range(1,x_length+1):
        for j in range(1,y_length+1):
            temp = [score[i-1,j-1]+rewardfun(s1[i-1],s2[j-1],0),score[i-1,j]+rewardfun(s1[i-1],s2[j-1],1),score[i,j-1]+rewardfun(s1[i-1],s2[j-1],2)]
            temp2 = max(temp)
            score[i, j] = temp2
            temp3 = temp.index(temp2)
            if temp3 == 0:
                pathx[i-1,j-1] = i-2
                pathy[i-1,j-1] = j-2
            elif temp3 == 1:
                pathx[i-1,j-1] = i-2
                pathy[i-1,j-1] = j-1
            else:
                pathx[i-1,j-1] = i-1
                pathy[i-1,j-1] = j-2
            file3.write(str([pathx[i-1,j-1],pathy[i-1,j-1]])+" "+"\t")
            file3.write(str(score[i,j])+" "+"\t")
        file3.write("\n")
    file3.close()

    file4 = open("align.txt","w")
    x = x_length-1
    y = y_length-1
    while x > 0 and y > 0:
        file4.write(str([x,y])+" "+str(score[x+1,y+1]))
        file4.write("\n")
        xp = pathx[x,y]
        yp = pathy[x,y]
        x = xp
        y = yp
    file4.write(str([x,y])+" "+str(score[x+1,y+1]))
    file4.write("\n")
    file4.close()

    return max(np.max(score[-2,:]),np.max(score[:,-2]))

def alignment(seq1, seq2):
    score = shortalign(seq1,seq2)
    print('score  : ' + str(score))
    file.write(str(score)+'\n')

file = open("result2.txt", "w")
past = time.time()
print('-------------')
count = 0
ccount = 0
dcount = 0
dccount = 0
#alignment(ecoli1, ecoli2)
#alignment(ecoli1, ecoli3)

for _ in range(10000):
    count1 = 0
    count2 = 0
    flag = 0
    # count3 = 0
    # seq1 = ecoli1
    # seq2 = ecoli2
    seq1 = np.random.randint(4, size=l_seqs)
    # seq2 = seq1
    #seq2 = np.random.randint(4, size=l_seqs2)

#    seq2 = np.mod(seq1 + (np.random.rand(l_seqs) < 0.088) * np.random.randint(4, size=l_seqs), 4)
    seq2 = np.mod(seq1 + (np.random.rand(l_seqs) < 0.33) * np.random.randint(4, size=l_seqs), 4)
    #print(seq2)
    seq2[0] = np.mod(seq1[0] + (np.random.randint(4, size=1)), 4)
    #print(seq2)
    for kk in range(l_seqs):
#        if np.random.rand() < 0.00014:
        if np.random.rand() < 0.0079:
            indel = zipfian(1.6, 10)
            ranval = np.random.rand()
            if ranval < 1 / 2:
                temp1 = seq1[0:kk + count1]
                temp4 = seq1[kk + count1:]
                seq1 = np.append(np.append(temp1, np.random.randint(4, size=indel)), temp4)
                count1 = count1 + 1
                if kk == 0:
                    flag = 1
            else:
                temp2 = seq2[0:kk + count2]
                temp5 = seq2[kk + count2:]
                seq2 = np.append(np.append(temp2, np.random.randint(4, size=indel)), temp5)
                count2 = count2 + 1
                if kk == 0:
                    flag = 2
    if seq1[0] != seq2[0]:
        array = [-1+align(seq1[1:], seq2[1:]),-1+align(seq1[1:], seq2[0:]),-1+align(seq1[0:], seq2[1:])]
        array2 = [-1+shortalign(seq1[1:], seq2[1:]),-1+shortalign(seq1[1:], seq2[0:]),-1+shortalign(seq1[0:], seq2[1:])]
        #print(array2)
        index = np.where(array == max(array))
        index2 = np.where(array2 == max(array2))
        if flag == 0:
            dcount += 1
        if min(index2[0]) in index[0]:
            count += 1
            ccount += 1
            if flag == 0:
                dccount += 1
            print("correct")
            print(array[flag])
            print(array2[flag])
            print(1-np.exp(-0.0008*n_length*(n_length-1)/(np.exp(0.223*array2[flag]))))
            print(dccount,dcount)
            print(ccount-dccount,count-dcount)
            print(_)
            print("------------------------")
        else:
            count += 1
            print(flag)
            print(index2[0])
            print(index[0])
            print("error")
            print(array[flag])
            print(array2[flag])
            print(1-np.exp(-0.0008*n_length*(n_length-1)/(np.exp(0.223*array2[flag]))))
            print(dccount,dcount)
            print(ccount-dccount,count-dcount)
            print(_)
            print("------------------------")
    now = time.time()
    file.write(str(now - past) + '\n')

print("time  : " + str(now - past))
file.close()