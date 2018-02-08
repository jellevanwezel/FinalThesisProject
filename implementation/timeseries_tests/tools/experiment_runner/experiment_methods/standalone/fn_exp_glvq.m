function [ results ] = fn_exp_glvq( dataset, glvqParams )

trainData = dataset.trainData;
trainLabels = dataset.trainLabels;
testData = dataset.testData;
testLabels = dataset.testLabels;

%classes = length(unique([trainLabels;testLabels]));
% Do experiment

if(~isfield(glvqParams, 'initialMatrix'))
    glvqParams.initialMatrix = eye(size(trainData,2));
end
    
glvqParams.learningRateMatrix = @(x) 0;
paramsAsCell = fn_exp_struct_to_input_cell(glvqParams);

[GLVQ_model,GLVQ_settting, trainError, ~, costs] = GMLVQ_train(trainData, trainLabels, paramsAsCell{:});

GLVQ_model.costs = costs;

estimatedTestLabels = GMLVQ_classify(testData, GLVQ_model);
testError = mean( testLabels ~= estimatedTestLabels );

results = struct('GLVQ_model',GLVQ_model,'GLVQ_setting',GLVQ_settting,'trainError',trainError,'testError',testError);
end

