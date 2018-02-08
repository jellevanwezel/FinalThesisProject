function [ results ] = fn_exp_suvrel_gml_gmlvq( dataset, gmlParams, gmlvqParams)

suvrelResults = fn_exp_suvrel(dataset);

gmlParams.initW = suvrelResults.g;

gmlResults = fn_exp_gml(dataset,gmlParams);

gmlvqParams.initialMatrix = gmlResults.W;

gmlvqResults = fn_exp_gmlvq( dataset, gmlvqParams);

results = struct('suvrel', suvrelResults, 'gml',gmlResults, 'gmlvq', gmlvqResults);

end
