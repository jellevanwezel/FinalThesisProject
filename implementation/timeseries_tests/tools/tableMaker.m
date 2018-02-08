t = StructArraySort(bestResultsAsArray,[1,2]);
allErrors = cell(8,16);
for i = 1:16:128
    s = t(i:i+15);
    for c = 1 : 16
        methodStruct =  s(c);
        errorStr = [num2str(methodStruct.testAVG), ' (', num2str(methodStruct.trainAVG),')'];
        allErrors{(i + 15) / 16, c} = errorStr;
    end
end