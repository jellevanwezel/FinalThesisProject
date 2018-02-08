function [ results ] = fn_exp_suvrel_gml( dataset, gmlParams)

% Read config
maxIter = gmlParams.maxIter;
stepSize = gmlParams.stepSize;

% Set default values
if(isempty(maxIter)); maxIter = 500; end;
if(isempty(stepSize)); stepSize = 10^-3; end;

trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;
[S,D] = fn_pre_SandD(trainData,trainLabels);

% Do experiments

% Get matrix from suvrel
gamma = 2 / (size(unique([testLabels;trainLabels]),1) - 1);
g = diag(suvrel(trainData,trainLabels,gamma,'none'));
% Get matrix and energies from gml
[W,energies] = adam_gml(g, trainData,trainLabels,S,D, maxIter,stepSize);

% Run classiefier
errors = zeros(2,1);
for j = 1:size(testData,1);
    label(1,1) = knnW(trainData,trainLabels,testData(j,:),3,W);
    label(2,1) = knng(trainData,trainLabels,testData(j,:),3,g);
    errors = errors + (label ~= testLabels(j));
end

% Save results;
errorRate = errors/size(testData,1);

results = struct('errorRate', errorRate, 'W', W, 'energies',energies, 'g', g);
end





 