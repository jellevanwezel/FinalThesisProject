function [ label ] = knnWL(data, labels, x, k, Ws)
    A = (data - repmat(x,[size(data,1),1]));
    dist = nan(size(data,1),1);
    for i = 1:size(data,1)
        W = Ws(:,:,labels(i));
        dist(i) = sqrt(A(i,:) * (W * (W' * A(i,:)'))); 
    end
    sorted = sortrows([dist,labels]);                       %Sort the rows
    label = mode(sorted(1:k,end));                          %Get the label of the majority of the top k
end
