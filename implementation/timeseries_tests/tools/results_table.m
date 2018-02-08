clear;

dataDir = '/home/jelle/Desktop/gml-new/';

dirFilePath = dir(dataDir);
fileNames = {dirFilePath.name};

resultTable = [];
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
    resStruct.trainAVG = 0;
    resStruct.testAVG = 0;
    
    methods = strsplit(resStruct.method,'_');
    
    resStruct.costs = cell(length(result.results),1);
    %resStruct.lowestCostEpoch = nan(length(result.results),1);
    %resStruct.firstCosts = nan(length(result.results),1);
    
    distances = cell(length(result.results), length(methods) - 1);
    
    for runIdx = 1 : length(result.results)
        
        curResult = result.results{runIdx,1};
        chainResult = curResult;
        
        modelNameArray = strsplit(resStruct.method,'_');
        methodName = modelNameArray{end};
        
        if isfield(curResult, methodName);curResult = getfield(curResult,methodName);end;
        if isa(curResult,'MException');skip=1;break;end;
        if length(curResult.trainError) == 1;skip=1;break;end;
        
        resStruct.trainAVG = resStruct.trainAVG + curResult.trainError(end);
        resStruct.testAVG = resStruct.testAVG + curResult.testError;
        
        modelName = [upper(modelNameArray{end}),'_model'];
        
        names = fieldnames(curResult);
        for nameIdx = 1 : length(names)
            if ~isempty(strfind(names{nameIdx},'_model'))
                modelName = names{nameIdx};
                break;
            end
        end
             
        
        %FNORMS
        
        
        curResult = result.results{runIdx,1};
        modelNameArray = strsplit(resStruct.method,'_');
        methodName = modelNameArray{end};
       
        
        
        if ~(length(modelNameArray) >= 2);resStruct.prefnorm = nan;resStruct.fnorm = nan;continue;end;
        if ~all(methodName(1,end-2:end) == 'lvq');resStruct.prefnorm = nan;resStruct.fnorm = nan;continue;end;
        
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
        if isfield(resStruct,'fdistance')
            resStruct.fdistance = resStruct.fdistance + abs(resStruct.prefnorm - resStruct.fnorm);
        else
            resStruct.fdistance = abs(resStruct.prefnorm - resStruct.fnorm);
        end
        
        
    end
    if isfield(resStruct,'fdistance')
        resStruct.fdistance = resStruct.fdistance / 10;
    else
        resStruct.fdistance = nan;
    end
    
%     distAvgs = cell(1,length(methods)-1);
%     for runIdx = 1 : size(distances,1)
%          for distIdx = 1 : size(distances,2)
%             distance = distances{runIdx,distIdx};
%             if iscell(distance)
%                 distance = cell2mat(distance);
%             end
%             if runIdx == 1
%                 distAvgs{1,distIdx} = distance;
%                 continue;
%             end
%             distAvgs{1,distIdx} = distAvgs{1,distIdx} + distance;
%          end
%     end
%     
%     for avgLengthIdx = 1:length(distAvgs)
%         distAvgs{1,avgLengthIdx} = distAvgs{1,avgLengthIdx} / length(result.results);
%     end
    
    resStruct.trainAVG = resStruct.trainAVG / length(result.results);
    resStruct.testAVG = resStruct.testAVG / length(result.results);
    %resStruct.startCostAVG = mean(resStruct.firstCosts);
    %resStruct.startCostSTD = std(resStruct.firstCosts);
    %resStruct.lowestCostEpochAVG = mean(resStruct.lowestCostEpoch);
    %resStruct.lowestCostEpochSTD = std(resStruct.lowestCostEpoch);
    %resStruct.matrixDistanceAVG = distAvgs;
    %resStruct.params = result.params;
    
    
    if skip;skip = 0;continue;end;
    
    resultTable = [resultTable,resStruct];
    
end