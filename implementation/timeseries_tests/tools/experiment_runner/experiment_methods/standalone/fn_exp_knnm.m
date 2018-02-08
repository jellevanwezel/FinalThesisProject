function [ results ] = fn_exp_knnm(dataset, knn_params )

trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

k = knn_params.k;
M = knn_params.M;

hits = zeros(max(k),1);

for i = 1:size(testData,1)        
        label = testLabels(i);
        x = testData(i,:);
        foundLabels = knn2M(trainData,trainLabels,k,x,M);
        hits = hits + (foundLabels == label);
end
hitRates = hits/size(testData,1);

results = struct('error',1-hitRates);

end