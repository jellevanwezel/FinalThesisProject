function [ weights ] = suvrell( data,labels, gamma,norm)
%Suvrell Finds the weights of the features in the data
%   data - the data points
%   labels - the labels indexed by its data points
%   gamma - the ratio between inner and outer classes (default 2)
%   norm - normalisation (default unity)


%the number of classes
n_classes = size(unique(labels),1);
%the unique class labels
classes = unique(labels);
%the amount of features
dim = size(data,2);
%the amount of classes
k = size(classes,1);

%initial matrix for the mean of the classes
mean_classes = zeros(n_classes,dim);

%for all the classes, calculate the means of the data
for i = 1:n_classes
   mean_classes(i,:) =  mean(data(labels == classes(i),:));
end

weights = zeros(n_classes,dim);

if ~(gamma == 2 &&  size(classes,2) == 2) %if gamma == 2 and k == 2 the first term can be omitted
    for i = 1 : n_classes
        classVar = var(data(labels == classes(i)),1);
        smeans = 0;
        for j = 1 : n_classes
            if i == j
                continue;
            end
            smeans = smeans + (mean_classes(classes(i),:) - mean_classes(classes(j),:)).^2;
        end
        weights(i,:) = (2-((k-1) * gamma)) * classVar  -  gamma * smeans;
    end
else
    %weights = smeans;
end

%Ensure the energy is larger than 0
weights(weights < 0) = 0;

%Normalize weights
if strcmp(norm,'unity')
    weights = weights / var(data);
end

if sum(weights .^ 2) == 0
    return;
end

for i = 1:n_classes
    %Find the weights from the energy.
    weights(i,:) = weights(i,:) ./ sqrt(sum(weights(i,:) .^2));
end


end


