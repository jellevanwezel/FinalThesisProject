function [ results ] = fn_exp_gml_gmlvq( dataset, gmlParams, gmlvqParams)


gmlResults = fn_exp_gml(dataset,gmlParams);

gmlvqParams.initialMatrix = gmlResults.W'; %Transposed because W = Omega^T

gmlvqResults = fn_exp_gmlvq( dataset, gmlvqParams);

results = struct('gml',gmlResults, 'gmlvq', gmlvqResults);

end
