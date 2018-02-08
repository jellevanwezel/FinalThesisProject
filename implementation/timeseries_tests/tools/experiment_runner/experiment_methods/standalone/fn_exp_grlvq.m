function [ results ] = fn_exp_grlvq( dataset, grlvqParams)

trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

if(isempty(grlvqParams.initialRelevances)); grlvqParams.initialRelevances = ones(1,size(trainData,2));end;

% Do experiment
paramsAsCell = fn_exp_struct_to_input_cell(grlvqParams);
[GRLVQ_model,GRLVQ_settting,trainError,~,costs] = GRLVQ_train(trainData, trainLabels, paramsAsCell{:});

GRLVQ_model.costs = costs;

estimatedTestLabels = GRLVQ_classify(testData, GRLVQ_model);
testError = mean( testLabels ~= estimatedTestLabels );

results = struct('GRLVQ_model',GRLVQ_model,'GRLVQ_setting',GRLVQ_settting,'trainError',trainError,'testError',testError);

end

