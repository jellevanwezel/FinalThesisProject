function [ label ] = knng(data, labels, x, k, g)
    A = (data - repmat(x,[size(data,1),1]));
    dist = nan(size(data,1),1);
    for i = 1:size(data,1)
        distSum = 0;
        for u = 1:size(data,2)
            for v = 1:size(data,2)
                 distSum = distSum + g(u,v) * A(i,u) * A(i,v);
            end
        end
        dist(i) = sqrt(distSum);
    end
    sorted = sortrows([dist,labels]);                       %Sort the rows
    label = mode(sorted(1:k,end));                          %Get the label of the majority of the top k
end

