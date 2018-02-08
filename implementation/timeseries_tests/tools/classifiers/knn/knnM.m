function [ label ] = knnM(data, labels, x, k, M)
    A = (data - repmat(x,[size(data,1),1]));
    dist = nan(size(data,1),1);
    for i = 1:size(data,1)
        dist(i) = A(i,:) * (M * A(i,:)'); 
    end
    sorted = sortrows([dist,labels]);                       %Sort the rows
    label = mode(sorted(1:k,end));                          %Get the label of the majority of the top k
end

