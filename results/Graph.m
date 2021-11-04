file = fopen('Hepatitis_1.txt','r');
rawseq1 = fscanf(file,'%s');
seq1 = (rawseq1=='A')+2*(rawseq1=='C')+3*(rawseq1=='G')+4*(rawseq1=='T');
fclose(file);
file = fopen('Hepatitis_3.txt','r');
rawseq2 = fscanf(file,'%s');
seq2 = (rawseq2=='A')+2*(rawseq2=='C')+3*(rawseq2=='G')+4*(rawseq2=='T');
fclose(file);

len = length(seq1);
len2 = length(seq2);

x = zeros(len,1);
y = zeros(len2,1);

score = zeros(len,len2);
index = cell(len,len2);
for i = 1:len
    for j = 1:len2
        if i == 1 && j ==1
            score(i,j) = 0;
            index{i,j} = [1,1];
        else
            if i == 1
                score(i,j) = score(i,j-1) - 2;
                index{i,j} = [i,j-1];
            else
                if j == 1
                    score(i,j) = score(i-1,j) - 2;
                    index{i,j} = [i-1,j-0];
                else
                    [score(i,j) temp] = max([score(i,j-1) - 2, score(i-1,j) - 2, score(i-1,j-1) + 3*(seq1(i)==seq2(j))-2]);
                    if temp == 1
                        index{i,j} = [i-0,j-1];
                    else
                        if temp == 2
                            index{i,j} = [i-1,j-0];
                        else
                            index{i,j} = [i-1,j-1];
                        end
                    end
                end
            end
        end
    end
    disp(i)
end

x2 = zeros(len,1);
y2 = zeros(len2,1);
tempx = len;
tempy = len2;
x2(1) = tempx;
y2(1) = tempy;
count = 1;
while tempx > 1 && tempy > 1
    count = count + 1;
    temp = index{tempx,tempy};
    tempx = temp(1);
    tempy = temp(2);
    x2(count) = tempx;
    y2(count) = tempy;
end
x2 = x2 - 1;
y2 = y2 - 1;
plot(x2(1:length(x2)-1),y2(1:length(y2)-1));