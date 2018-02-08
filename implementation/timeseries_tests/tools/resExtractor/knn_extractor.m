clear;

dataDir = '/home/jelle/Desktop/knn_data/';

dirFilePath = dir(dataDir);
fileNames = {dirFilePath.name};

resultTable = [];
skip = 0;

for fileIdx = 3 : length(fileNames)
    
    fileStruct = dirFilePath(fileIdx);
    load([dataDir,fileStruct.name]);
    disp([dataDir,fileStruct.name]);
    
    [avgError,k] = get_knn_AvgError(result );
    
    resultTable = [resultTable;struct(...
        'dataset', result.dataSetName,...
        'method', result.function(8:end),...
        'pre', result.preprocessing(8:end),...       
        'errorAVG',avgError,...
        'k',k...
        )];
      
end