import numpy as np

file = open('result4.txt','r')

temp = 1
count = -1
name= []
match = []
data = 0
while temp:
    temp = file.readline().replace('\n','')
    if temp:
        if 'Reverse' in temp:
            continue
        elif '>' in temp:
            count += 1
            name.append(temp.replace(' ','').replace('>',''))
            match.append(data)
            data = 0
        elif '#' in temp:
            continue
        else:
            temp2 = temp.split()
            data += int(temp2[2])
        
match.append(data)
match = match[1:]