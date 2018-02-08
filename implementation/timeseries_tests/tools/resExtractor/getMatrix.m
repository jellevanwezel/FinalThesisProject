function [ W ] = getMatrix( runResult, methodName )

matrixName = matrixMap(methodName);
if all(methodName(1,end-2:end) == 'lvq')
    runResult = modelFinder( runResult, methodName);
end
W = getfield(runResult,matrixName);

%in case of suvrell
if size(size(W),2) == 3
    tempW = cell(1,size(W,3));
    for matIdx = 1 : size(W,3)
        tempW{1,matIdx} = W(:,:,matIdx);
    end
    W = tempW;
end

if ~iscell(W)
    W = {W};
end

end

