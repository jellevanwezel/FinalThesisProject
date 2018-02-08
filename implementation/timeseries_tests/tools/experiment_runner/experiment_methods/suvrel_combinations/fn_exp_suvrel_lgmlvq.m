function [ results ] = fn_exp_suvrel_lgmlvq( dataset, lgmlvqParams )

uniqueLabels = length(unique([dataset.trainLabels;dataset.testLabels]));
suvrelResults = fn_exp_suvrel(dataset);


initialMatrices = cell(1,uniqueLabels);

for i = 1 : uniqueLabels
    initialMatrices{1,i} = suvrelResults.g;
end


lgmlvqParams.initialMatrices = initialMatrices;
lgmlvqResults = fn_exp_lgmlvq( dataset, lgmlvqParams);

results = struct('suvrel', suvrelResults, 'lgmlvq', lgmlvqResults);

end

