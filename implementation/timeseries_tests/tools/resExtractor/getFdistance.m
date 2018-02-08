function [md1,sd1,md2,sd2 ] = getFdistance(result, methodNames )

if length(methodNames) < 2
    md1 = [];
    md2 = [];
    sd1 = [];
    sd2 = [];
    return;
end

runs = length(result.results);
distances1 = [];
distances2 = [];

for runIdx = 1 : runs
    
    matrices = cell(length(methodNames),1);
    
    for methodIdx = 1 : length(methodNames)
        methodName = methodNames{1,methodIdx};
        runResult = result.results{runIdx,1};
        runResult = getfield(runResult,methodName);
        matrices{methodIdx,1} = getMatrix(runResult, methodName);      
    end
    
    distances1 = [distances1; calcFdistances( matrices{1,1}, matrices{2,1} )];
    
    if(length(methodNames) > 2)
        distances2 = [distances2; calcFdistances( matrices{2,1}, matrices{3,1} )];
    end
end

md1 = mean(distances1);
md2 = mean(distances2);
sd1 = std(distances1);
sd2 = std(distances2);
