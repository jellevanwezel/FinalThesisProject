function [ results ] = fn_exp_suvrel_grlvq( dataset, grlvqParams )

suvrelResults = fn_exp_suvrel(dataset);

initialRelevances = diag(suvrelResults.g);
grlvqParams.initialRelevances = initialRelevances';

grlvqResults = fn_exp_grlvq( dataset, grlvqParams);

results = struct('suvrel', suvrelResults, 'grlvq', grlvqResults);
end

