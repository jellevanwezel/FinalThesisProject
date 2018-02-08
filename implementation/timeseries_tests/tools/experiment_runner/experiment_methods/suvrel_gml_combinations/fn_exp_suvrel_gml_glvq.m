function [ results ] = fn_exp_suvrel_gml_glvq( dataset, gmlParams, glvqParams)

suvrelResults = fn_exp_suvrel(dataset);

gmlParams.initW = suvrelResults.g;

gmlResults = fn_exp_gml(dataset,gmlParams);

W = gmlResults.W;
glvqParams.initialMatrix = W;

glvqResults = fn_exp_glvq( dataset, glvqParams);

results = struct('suvrel', suvrelResults, 'gml',gmlResults, 'glvq', glvqResults);

end
