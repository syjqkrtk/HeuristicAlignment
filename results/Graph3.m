xlabel('score');
ylabel('n');
hold on
for i = 1:5
    for j = 1:81
        result2(j,i) = sum(result(:,i)==j-21); % 1010
    end
end

mn = [10000,40000,90000,160000,250000];
lambda = 0.001:0.001:1;
K = 0.0001:0.0001:0.1;
result3 = zeros(1000,1000);

for l = 1:1000
    disp(l);
    for k = 1:1000
        for i = 1:5
            for j = 1:81
                fitsco = exp(-K(k)*mn(i)*exp(-lambda(l)*(j-21)))-exp(-K(k)*mn(i)*exp(-lambda(l)*(j-22)));
%                 disp(fitsco);
                result3(l,k) = result3(l,k) + (99*fitsco-result2(j,i))^2;
            end
        end
    end
end

[minval, index] = min(result3);
[minval2, index2] = min(minval);
K = K(index2);
lambda = lambda(index(index2));

histogram(result(:,1));
histogram(result(:,2));
histogram(result(:,3));
histogram(result(:,4));
histogram(result(:,5));

x = -20:60;
y = exp(-K*mn(1)*exp(-lambda*(x)))-exp(-K*mn(1)*exp(-lambda*(x-1)));
plot(x,y*99);
y = exp(-K*mn(2)*exp(-lambda*(x)))-exp(-K*mn(2)*exp(-lambda*(x-1)));
plot(x,y*99);
y = exp(-K*mn(3)*exp(-lambda*(x)))-exp(-K*mn(3)*exp(-lambda*(x-1)));
plot(x,y*99);
y = exp(-K*mn(4)*exp(-lambda*(x)))-exp(-K*mn(4)*exp(-lambda*(x-1)));
plot(x,y*99);
y = exp(-K*mn(5)*exp(-lambda*(x)))-exp(-K*mn(5)*exp(-lambda*(x-1)));
plot(x,y*99);