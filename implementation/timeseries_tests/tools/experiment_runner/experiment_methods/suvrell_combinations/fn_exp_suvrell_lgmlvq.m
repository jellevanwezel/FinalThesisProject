function [ results ] = fn_exp_suvrell_lgmlvq( dataset, suvrellParmas, lgmlvqParams )

suvrellResults = fn_exp_suvrell(dataset,suvrellParmas);


initialMatrices = cell(1,size(suvrellResults.g, 3));

%todo refactor this to one line no loop :D
for i = 1 : size(suvrellResults.g, 3)
    initialMatrices{1,i} = suvrellResults.g(:,:,i);
end


lgmlvqParams.initialMatrices = initialMatrices;
lgmlvqResults = fn_exp_lgmlvq( dataset, lgmlvqParams);
results = struct('suvrell', suvrellResults, 'lgmlvq', lgmlvqResults);

end

