function [ results ] = fn_exp_suvrel_gml_lgmlvq( dataset, gmlParams, lgmlvqParams)

uniqueLabels = length(unique([dataset.trainLabels;dataset.testLabels]));

suvrelResults = fn_exp_suvrel(dataset);

gmlParams.initW = suvrelResults.g;

gmlResults = fn_exp_gml(dataset,gmlParams);

initialMatrices = cell(1,uniqueLabels);

for i = 1 : uniqueLabels
    initialMatrices{1,i} = gmlResults.W;
end

lgmlvqParams.initialMatrices = initialMatrices;

lgmlvqResults = fn_exp_lgmlvq( dataset, lgmlvqParams);

results = struct('suvrel', suvrelResults, 'gml',gmlResults, 'lgmlvq', lgmlvqResults);

end
