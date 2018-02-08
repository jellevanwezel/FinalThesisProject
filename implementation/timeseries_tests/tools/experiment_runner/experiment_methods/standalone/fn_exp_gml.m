function [ results ] = fn_exp_gml(dataset, gmlParams)

% Read config
initW = gmlParams.initW;
maxIter = gmlParams.maxIter;
stepSize = gmlParams.stepSize;

% Set default values
if(isempty(initW)); initW = eye(size(dataset.trainData,2)); end;
if(isempty(maxIter)); maxIter = 500; end;
if(isempty(stepSize)); stepSize = 10^-3; end;


trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;
[S,D] = fn_pre_SandD(trainData,trainLabels);

% Do experiments

% Get matrix from gml
[W,energies] = adam_gml(initW, trainData,trainLabels,S,D, maxIter,stepSize);

% Run classiefier
errors = 0;
for j = 1:size(testData,1);
    label = knnW(trainData,trainLabels,testData(j,:),3,W);
    errors = errors + (label ~= testLabels(j));
end

% Save results;
errorRate = errors/size(testData,1);

results = struct('errorRate', errorRate, 'W', W, 'energies',energies);
end

