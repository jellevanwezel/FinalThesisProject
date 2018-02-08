clear;

dataDir = '/home/jelle/Desktop/data/';

dirFilePath = dir(dataDir);
fileNames = {dirFilePath.name};

fnormTable = [];
skip = 0;

dataSizeMap = struct(...
'bal',4,...
'bre',9,...
'iri',4,...
'par',22,...
'pim',8,...
'see',7,...
'seg',19,...
'win',13 ...
);

matrixMap = struct(...
'suvrel','g', ...
'gml','W', ...
'glvq','omega', ...
'grlvq','lambda', ...
'gmlvq','omega', ...
'lgmlvq','psis', ...
'suvrell','g' ...
);

for fileIdx = 3 : length(fileNames)
    
    fileStruct = dirFilePath(fileIdx);
    load([dataDir,fileStruct.name]);
    
    disp([dataDir,fileStruct.name]);
    
    resStruct = struct();
    resStruct.dataset = result.dataSetName;
    resStruct.method = result.function(8:end);
    resStruct.pre = result.preprocessing(8:end);    

    
    
    for runIdx = 1 : 1% length(result.results)
        
        curResult = result.results{runIdx,1};
        modelNameArray = strsplit(resStruct.method,'_');
        methodName = modelNameArray{end};
        
        if ~(length(modelNameArray) == 2);skip = 1;break;end;
        if ~all(methodName(1,end-2:end) == 'lvq');skip = 1;break;end;
        if isa(curResult,'MException');skip=1;break;end;
        preName = modelNameArray{end-1};
        preResult = getfield(curResult,preName);
        curResult = getfield(curResult,methodName);
        
        % lvq method and 2 methods
        
        % get model name
        
        
        %pre fnorms and traces
        
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
    if skip; skip = 0;continue;end;
    fnormTable = [fnormTable,resStruct];
    
end