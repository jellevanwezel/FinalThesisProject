function [ results ] = fn_exp_suvrel_gmlvq( dataset, gmlvqParams )

suvrelResults = fn_exp_suvrel(dataset);

gmlvqParams.initialMatrix = suvrelResults.g;

gmlvqResults = fn_exp_gmlvq( dataset, gmlvqParams);

results = struct('suvrel', suvrelResults, 'gmlvq', gmlvqResults);

end

