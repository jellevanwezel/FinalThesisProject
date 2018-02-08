function [ results ] = fn_exp_gml_knnm( dataset, gmlParams, knnm_params)

gmlResults = fn_exp_gml(dataset,gmlParams);

W = gmlResults.W;

M = W*W'; %W' because W' =  Omega

knnm_params.M = M;

knnResults = fn_exp_knn(dataset, knnm_params );

results = struct('gml',gmlResults, 'knnm', knnResults);

end


