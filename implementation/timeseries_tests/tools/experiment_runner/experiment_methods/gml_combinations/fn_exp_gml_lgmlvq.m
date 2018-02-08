function [ results ] = fn_exp_gml_lgmlvq( dataset, gmlParams, lgmlvqParams)

uniqueLabels = length(unique([dataset.trainLabels;dataset.testLabels]));

gmlResults = fn_exp_gml(dataset,gmlParams);

initialMatrices = cell(1,uniqueLabels);

for i = 1 : uniqueLabels
    initialMatrices{1,i} = gmlResults.W';%Transposed because W = Omega^T
end

lgmlvqParams.initialMatrices = initialMatrices;

lgmlvqResults = fn_exp_lgmlvq( dataset, lgmlvqParams);

results = struct('gml',gmlResults, 'lgmlvq', lgmlvqResults);

end
