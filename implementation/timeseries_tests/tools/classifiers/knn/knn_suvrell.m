function [ label ] = knn_suvrell(data, labels, xs, k)
    WsSize = size(unique(labels),1);
    dists = nan(size(data,1),1);
    
    for WIndex = 1 : WsSize
       classData = data(labels == WIndex,:);
       x = xs(WIndex,:);
       dists(labels == WIndex,1) = sqrt(sum((classData - repmat(x,size(classData,1),1)).^2,2));
    end
    
    sorted = sortrows([dists,labels]);
    label = mode(sorted(1:k,end));
end
