function [ results ] = fn_exp_gmlvq( dataset, gmlvqParams)
    
trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

gmlvqParams.optimization = 'sgd';

if isempty(gmlvqParams.initialMatrix)
    gmlvqParams.initialMatrix = eye(size(trainData,2));
end

% Do experiment

% Todo: fix the struct here to pass all parameters

paramsAsCell = fn_exp_struct_to_input_cell(gmlvqParams);
[GMLVQ_model,GMLVQ_settting, trainError, ~, costs] = GMLVQ_train(trainData, trainLabels, paramsAsCell{:});

GMLVQ_model.costs = costs;

estimatedTestLabels = GMLVQ_classify(testData, GMLVQ_model);
testError = mean( testLabels ~= estimatedTestLabels );



results = struct('GMLVQ_model',GMLVQ_model,'GMLVQ_setting',GMLVQ_settting,'trainError',trainError,'testError',testError);

end

