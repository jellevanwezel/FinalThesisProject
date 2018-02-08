function [ results ] = fn_exp_lgmlvq( dataset, lgmlvqParams)
    
trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

if isempty(lgmlvqParams.initialMatrices)
    lgmlvqParams.initialMatrices = cell(size(trainData,2),1);
    for i = 1:size(trainData,2)
        lgmlvqParams.initialMatrices{i,1} = eye(size(trainData,2));
    end
end

% Do experiment
paramsAsCell = fn_exp_struct_to_input_cell(lgmlvqParams);
[LGMLVQ_model,LGMLVQ_settting,trainError,~,costs] = LGMLVQ_train(trainData, trainLabels, paramsAsCell{:});

LGMLVQ_model.costs = costs;

estimatedTestLabels = LGMLVQ_classify(testData, LGMLVQ_model);
testError = mean( testLabels ~= estimatedTestLabels );

results = struct('lGMLVQ_model',LGMLVQ_model,'lGMLVQ_setting',LGMLVQ_settting,'trainError',trainError,'testError',testError);

end

