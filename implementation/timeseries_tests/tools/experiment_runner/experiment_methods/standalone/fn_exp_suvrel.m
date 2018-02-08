function [ results ] = fn_exp_suvrel(dataset)
    
%todo:
    %weave params through here
    %alpha
    %normalisation of the results
    
trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

% Do experiment

% Get matrix from suvrel
gamma = 2 / (size(unique([trainLabels;testLabels]),1) - 1);
g = diag(suvrel(trainData,trainLabels,gamma,'none'));

% Run classiefier
errors = 0;
for j = 1:size(testData,1);
    label = knng(trainData,trainLabels,testData(j,:),3,g);
    errors = errors + (label ~= testLabels(j));
end
% Save results;
errorRate = errors/size(testData,1);

results = struct('errorRate', errorRate, 'g', g);
end

