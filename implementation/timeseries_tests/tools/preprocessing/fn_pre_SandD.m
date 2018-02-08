function [ S, D ] = createSandD(data,labels)
ulabels = unique(labels);
Dcombinations = nchoosek(ulabels,2);
ldata = [data,labels];

S=[];
for i = 1:size(ulabels,1)
    label = ulabels(i);
    cluster = nchoosek(find(ldata(:,end) == label),2);
    if size(cluster,2) == 2
        S = [S;cluster];
    end
end

D = [];
for i = 1 : size(Dcombinations,1)
    groupi = find(ldata(:,end) == Dcombinations(i,1))';
    groupj = find(ldata(:,end) == Dcombinations(i,2))';
    D = [D; combvec(groupi,groupj)'];
end

