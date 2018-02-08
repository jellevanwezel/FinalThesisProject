function [combParams] = fn_exp_paramCombs(params)
psize = size(params,2);
cellCombs = cell(1,psize);
for i = 1:psize    
    paramCell = params{1,i};
    pCellSize = size(paramCell,1);
    cellCombs{1,i} = 1:pCellSize;
end
combinations = combvec(cellCombs{:})';

combParams = cell(size(combinations));

for i = 1:size(combinations,1)
    combRow = combinations(i,:);
    for j = 1:size(combinations,2)
        structVect = params{j};
        combParams{i,j} = structVect{combRow(j)};
    end
end

end
