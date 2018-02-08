function [ weights ] = suvrel( data,labels, gamma,norm)
%Suvrel Finds the weights of the features in the data
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

%initial matrix for the mean of the classes
mean_classes = zeros(n_classes,dim);

%for all the classes, calculate the means of the data
for i = 1:n_classes
   mean_classes(i,:) =  mean(data(labels == classes(i),:));
end

%sum of the means of the classes classes
smeans = zeros(1,dim); 

%get all combinations of classes in pairs of 2
combinations = nchoosek(classes,2);

%for each combination...
for i = 1:size(combinations,1)
    %take the first of the pair
    a = combinations(i,1);
    %take the seccond of the pair
    b = combinations(i,2);
    %calculate the sum of of the distance between all the means of the pairs (squared)
    smeans = smeans + (mean_classes(classes(a),:) - mean_classes(classes(b),:)).^2; 
end

if gamma ~= 2
    var_classes = zeros(n_classes,dim);
    for i = 1 : n_classes
        var_classes(i,:) = var(data(labels == classes(i),:));
    end
    svar = sum(var_classes,1); %sum varince classes
    weights = ((gamma - 2) * svar  +  gamma / ( n_classes - 1) * smeans);
else
    weights = smeans;
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

%Find the weights from the energy.
weights = weights / sqrt(sum(weights .^ 2));

end
