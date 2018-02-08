function [ labels ] = knn2M(data, labels,ks, x, M)
distances = nan(size(data,1),1);
for i=1:size(data,1)
    distances(i,1) = (data(i,:) - x)' * M * (data(i,:) - x);
end
sorted = sortrows([distances,labels],1);
labels = nan(size(ks,2),1);
for k = 1:size(ks,2)
    labels(k) = mode(sorted(1:k,end),1);
end
end

