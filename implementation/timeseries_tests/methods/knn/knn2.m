function [ labels ] = knn2(data, labels,ks, x, distM)
distances = pdist2(data,x,distM);
sorted = sortrows([distances,labels],1);
labels = nan(size(ks,2),1);
for k = 1:size(ks,2)
    labels(k) = mode(sorted(1:k,end),1);
end
end

