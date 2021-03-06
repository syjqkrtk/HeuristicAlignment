x = 1:200;
% y = 1-exp(-0.0020*(x.*(x-1))./exp(0.1585*x));
% y = 1-exp(-0.0013*(x.*(x-1))./exp(0.1320*x));
% y = 1-exp(-0.0008*(x.*(x-1))./exp(0.223*x*(1-0.25-0.0079*(4.45/1.88))));
% y2 = 1-exp(-0.0004*(x.*(x-1))./exp(0.223*x*(1-0.25-0.0079*(4.45/1.88)))).*(0.25*exp(-0.000625*(x-1).^2./exp(0.223*x*(1-0.25-0.0079*(4.45/1.88))))+0.75*exp(-0.0004*(x-1).^2./exp(0.223*x*(1-0.25-0.0079*(4.45/1.88)))));
% plot(x,y);
hold on
% plot(x,y2);
z = [1 2 3 5 10 20 30 50 100 200];
% p = [0.0743 0.0748 0.0844 0.0680 0.0684 0.0551];
% p = [0.0149 0.0242 0.0161 0.00680 0.0259 0.00973];
% p = [0 0.00752 0.00991 0.0189 0.0339 0.0325 0.0187 0.00730 0 0];
p = [0 0.00752 0.00991 0.135 0.0339 0.058 0.106 0.0565 0.0449 0.0460];
% p2 = [0.0618 0.0206 0.0207 0.0119 0.000472 0];
temp = zeros(10000,10000);
for A = 1:10000
    for B = 1:10000
        for i = 1:6
            y = 1-exp(-A/10000*(z(i).*(z(i)-1))./exp(B/10000*z(i)));
            temp(A,B) = temp(A,B) + (y - p(i))^2;
        end
    end
    disp(A)
end
    
% p = [0.0058 0.0054 0.00213 0 0.00144 0];
% p2 = [0 0 0 0 0 0];
% p = [0.0183 0.0099 0.0085 0.0236 0.0192 0];
% p2 = [0.056 0.214 0 0.08 0 0];
plot(z,p);
% plot(z,p2);
% legend('analysis(SNP)', 'analysis(indel)', 'simulation(SNP)', 'simulation(indel)');
legend('Simulation');