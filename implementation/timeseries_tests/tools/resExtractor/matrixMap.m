function [ matrixName ] = matrixMap(methodName)
matrixMap = struct(...
'suvrel','g', ...
'gml','W', ...
'glvq','omega', ...
'grlvq','lambda', ...
'gmlvq','omega', ...
'lgmlvq','psis', ...
'suvrell','g' ...
);
matrixName = getfield(matrixMap,methodName);
end

