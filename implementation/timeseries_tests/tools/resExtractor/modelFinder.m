function [ model ] = modelFinder( runResult, methodName )

modelNameArray = strsplit(methodName,'_');
methodName = modelNameArray{end};
if isfield(runResult, methodName);runResult = getfield(runResult,methodName);end;
      
names = fieldnames(runResult);
for nameIdx = 1 : length(names)
    if ~isempty(strfind(names{nameIdx},'_model'))
        modelName = names{nameIdx};
        break;
    end
end

model = getfield(runResult,modelName);

end

