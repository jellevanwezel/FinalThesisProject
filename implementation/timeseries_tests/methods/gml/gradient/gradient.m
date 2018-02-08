function [ gradients ] = gradient(S,D,W, data,a)
%S are the indexes of the same class data points in data, [datapoint1, datapoint2]
%D are the indexes of the different class data points in data [datapoint1, datapoint2]
%W : M = WW'
%data is the data
%a is the ratio between same and different classes usualy 0.9
%gradients are the calculated gradients for every wk: [dEW/dw1, dEW/dw2, dEW/dw..., dEW/dwk]'

gradients = zeros(size(W));

for k = 1:size(W,2);
    wk = W(:,k);
    sumD = 0;
    sumS = 0;
    for index = 1:size(S,1)
        xi = data(S(index,1),:)';
        xj = data(S(index,2),:)';
        A = xi - xj;
        sumS = sumS + ((wk' * A) * A);
    end
    for index = 1:size(D,1)
        xi = data(D(index,1),:)';
        xj = data(D(index,2),:)';
        A = xi - xj;
        dist = sqrt(A' * (W * (W' * A)));
        sumD = sumD + ((1 - min([dist,1]))/dist) * ((wk' * A) * A);
    end
    gradients(:,k) = -2 * a * sumD + 2 * (1-a) * sumS;
end

