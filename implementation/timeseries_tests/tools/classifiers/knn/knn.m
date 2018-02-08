function [ label ] = knn(data, labels, x, k)
    dist = sqrt((data - repmat(x,[size(data,1),1])).^2);    %Calculate the distance
    sorted = sortrows([dist,labels]);                       %Sort the rows
    label = mode(sorted(1:k,end));                          %Get the label of the majority of the top k
end

