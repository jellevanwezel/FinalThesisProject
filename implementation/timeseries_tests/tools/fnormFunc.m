function [ output_args ] = fnormFunc( input_args )

matrixMap = struct(...
'suvrel','g', ...
'gml','W', ...
'glvq','omega', ...
'grlvq','lambda', ...
'gmlvq','omega', ...
'lgmlvq','psis', ...
'suvrell','g' ...
);

W = getfield(preResult,getfield(matrixMap,preName));

if size(size(W),2) == 3
    traces = nan(1,length(W));
    tracesAfterNorm = nan(1,length(W));
    fnorms = nan(1,length(W));
    for WIdx = 1 : size(W,3)
        cW = W(:,:,WIdx);
        if size(cW,1) ~= size(cW,2); cW = diag(cW);end;
        traces(WIdx) = trace(cW);
        cW = cW/trace(cW);
        tracesAfterNorm(WIdx) = trace(cW);
        fnorms(WIdx) = norm(cW'*cW,'fro');
    end
    %resStruct.pretrace = traces;
    %resStruct.pretraceAfterNorm = tracesAfterNorm;
    resStruct.prefnorm = fnorms;
else
    if size(W,1) ~= size(W,2); W = diag(W);end;
    %resStruct.pretrace = trace(W);
    W = W/trace(W);
    %resStruct.pretraceAfterNorm = trace(W);
    resStruct.prefnorm = norm(W'*W,'fro');
end 

%lvq fnorms and traces

names = fieldnames(curResult);
for nameIdx = 1 : length(names)
    if ~isempty(strfind(names{nameIdx},'_model'))
        modelName = names{nameIdx};
        break;
    end
end
model = getfield(curResult,modelName);
W = getfield(model,getfield(matrixMap,methodName));

if iscell(W)
    traces = nan(1,length(W));
    tracesAfterNorm = nan(1,length(W));
    fnorms = nan(1,length(W));
    for WIdx = 1 : length(W)
        cW = W{WIdx};
        if size(cW,1) ~= size(cW,2); cW = diag(cW);end;
        traces(WIdx) = trace(cW);
        cW = cW/trace(cW);
        tracesAfterNorm(WIdx) = trace(cW);
        fnorms(WIdx) = norm(cW'*cW,'fro');
    end
    %resStruct.trace = traces;
    %resStruct.traceAfterNorm = tracesAfterNorm;
    resStruct.fnorm = fnorms;
else
    if size(W,1) ~= size(W,2); W = diag(W);end;
    %resStruct.trace = trace(W);
    W = W/trace(W);
    %resStruct.traceAfterNorm = trace(W);
    resStruct.fnorm = norm(W'*W,'fro');
end
if length(resStruct.prefnorm) ~= length(resStruct.fnorm);skip=1;break;end;
resStruct.fdistance = abs(resStruct.prefnorm - resStruct.fnorm);
end

