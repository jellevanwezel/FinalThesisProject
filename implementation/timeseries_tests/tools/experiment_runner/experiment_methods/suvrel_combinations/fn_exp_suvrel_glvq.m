function [ results ] = fn_exp_suvrel_glvq( dataset, glvqParams )

%todo the glvq method does not yet exist

suvrelResults = fn_exp_suvrel(dataset);

%todo modify the data such that glvq uses the transformed data from suvrel
g = suvrelResults.g;
glvqParams.initialMatrix = g;

glvqResults = fn_exp_gmlvq( dataset, glvqParams);

results = struct('suvrel', suvrelResults, 'glvq', glvqResults);

end

