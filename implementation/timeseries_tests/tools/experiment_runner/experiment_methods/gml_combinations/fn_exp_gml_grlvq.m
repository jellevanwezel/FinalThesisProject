function [ results ] = fn_exp_gml_grlvq( dataset, gmlParams, grlvqParams)

gmlResults = fn_exp_gml(dataset,gmlParams);

initialRelevances = diag(gmlResults.W)';
grlvqParams.initialRelevances = initialRelevances;

grlvqResults = fn_exp_grlvq( dataset, grlvqParams);

results = struct('gml',gmlResults, 'grlvq', grlvqResults);

end
