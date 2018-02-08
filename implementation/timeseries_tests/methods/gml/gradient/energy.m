function [ E ] = energy( data,S,D, a,W )

sumD = 0;
sumS = 0;

for index = 1: S
   xi = data(S(index,1),:)';
   xj = data(S(index,2),:)';
   A = xi - xj;
   dist = sqrt(A' * (W * (W' * A)));
   sumS = sumS + dist^2;
end

for index = 1: D
   xi = data(D(index,1),:)';
   xj = data(D(index,2),:)';
   A = xi - xj;
   dist = sqrt(A' * (W * (W' * A)));
   sumD = sumD + (1-min([dist,1]))^2; 
end

E = a * sumD + (1-a) * sumS;

end

