function [ results ] = fn_exp_suvrell(dataset, suvrellParams)
    
%todo fix this, no struct :)
trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

gamma = suvrellParams.gamma;

uniqueLabels = unique([testLabels;trainLabels]);    
g = nan(size(trainData,2),size(trainData,2),size(uniqueLabels,1));

% Do experiments

% Get matrix from suvrel

classWeights = suvrell(trainData,trainLabels,gamma,'none');
for classIndex = 1:size(uniqueLabels,1)
    g(:,:,classIndex) = diag(classWeights(classIndex,:));
end


% Prepair data
transformedData = nan(size(trainData,1),size(trainData,2));
rowCount = 1;
for l = 1:size(uniqueLabels,1)
    classData = trainData(trainLabels == l,:);
    for row = 1:size(classData,1)
        transformedData(rowCount,:) = classData(row,:) * sqrt(g(:,:,l))';
        rowCount = rowCount + 1;
    end
end

% Run classiefier
errors = 0;
for j = 1:size(testData,1);
    x = testData(j,:);
    xs = nan(size(uniqueLabels,1),size(trainData,2));
    for gIndex = 1 : size(uniqueLabels,1)
        xs(gIndex,:) = x * sqrt(g(:,:,gIndex))';
    end
    %classificationData = reshape(classMeans,1,size(data,2),size(uniqueLabels,1));
    label = knn_suvrell(transformedData,trainLabels,xs, 3);
    errors = errors + (label ~= testLabels(j));
end

% Save results;
errorRate = errors/size(testData,1);
    
results = struct('errorRate', errorRate, 'g', g);
end

