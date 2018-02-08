function [ results ] = fn_exp_suvrel_gml_grlvq( dataset, gmlParams, grlvqParams)

suvrelResults = fn_exp_suvrel(dataset);

gmlParams.initW = suvrelResults.g;

gmlResults = fn_exp_gml(dataset,gmlParams);

initialRelevances = diag(gmlResults.W);
grlvqParams.initialRelevances = initialRelevances;

grlvqResults = fn_exp_grlvq( dataset, grlvqParams);

results = struct('suvrel', suvrelResults, 'gml',gmlResults, 'grlvq', grlvqResults);

end
