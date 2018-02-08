function [ results ] = fn_exp_knn(dataset, knn_params )

trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

k = knn_params.k;
distanceMeasure = knn_params.distanceMeasure;

hits = zeros(max(k),1);

for i = 1:size(testData,1)        
        label = testLabels(i);
        x = testData(i,:);
        foundLabels = knn2(trainData,trainLabels,k,x,distanceMeasure);
        hits = hits + (foundLabels == label);
end
hitRates = hits/size(testData,1);

results = struct('error',1-hitRates);

end

