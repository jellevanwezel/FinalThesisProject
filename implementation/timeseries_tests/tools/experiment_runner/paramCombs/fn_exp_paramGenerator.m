function [ params ] = fn_exp_paramGenerator( statics, ranges )

rangeNames = fieldnames(ranges);
staticNames = fieldnames(statics);
rangeCell = cell(1,size(rangeNames,1));
staticCell = cell(1,size(staticNames,1));



for i = 1 : size(staticNames,1)
    %staticCell{1,i} = getfield(statics,staticNames{i});
    staticCell{1,i} = 1;
end

for i = 1 : size(rangeNames,1) 
    fieldValue = getfield(ranges,rangeNames{i});
    rangeCell{1,i} = 1:size(fieldValue,2);
end

% -- Dark magick starts here, don't ask --
staticRanges = [staticCell,rangeCell];
combinations = combvec(staticRanges{:})';
%create combinations of the placeholder vectors

params = cell(size(combinations,1),1);
for i = 1:size(combinations,1)
    %for each combination
    paramComb = struct();
    
    %substitude the placeholders for the real static values
    for j = 1:size(staticCell,2)
        paramComb = setfield(paramComb, staticNames{j},getfield(statics,staticNames{j}));
    end
    
    %substitude the placeholders for the real range values
    for j = 1 : size(rangeCell,2)
        range = getfield(ranges,rangeNames{j});
        combValue = combinations(i,j + size(staticCell,2));
        
        %can be a cell or a vector
        if iscell(range)
            paramComb = setfield(paramComb,rangeNames{j},range{1,combValue});
        else
            paramComb = setfield(paramComb,rangeNames{j},range(1,combValue));
        end
    end
    
    %add this combination to the parameters list
    params{i,1} = paramComb;
end