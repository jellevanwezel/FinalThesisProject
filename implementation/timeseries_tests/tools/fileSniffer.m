clear;

destination = '/home/jelle/Desktop/data/';
rootFilePath = '/home/jelle/RUG/RI/remote-results';
subDirs = {rootFilePath};

while length(subDirs) ~= 0
    currentFilePath = subDirs{1};
    dirFilePath = dir(currentFilePath);
    subDirs(1) = [];
    fileNames = {dirFilePath.name};
    
    for fileIdx = 3 : length(fileNames);
        fileStruct = dirFilePath(fileIdx);
        fileName = fileNames{fileIdx};
        filePath = [currentFilePath,'/',fileName];
        
        if fileStruct.isdir
            subDirs = [subDirs, {filePath}];
        else
            dates = {'10-Oct','11-Oct','12-Oct','13-Oct','14-Oct','15-Oct','16-Oct','17-Oct','18-Oct','19-Oct','20-Oct'};
            for dateIdx = 1 : length(dates)
                if ~isempty(strfind(fileName,dates{dateIdx}))
                    copyfile(filePath,destination);
                    break;
                end
            end 
        end
        
    end

end

