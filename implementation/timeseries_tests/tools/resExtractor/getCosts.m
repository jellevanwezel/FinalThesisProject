function [ AVGcosts, costs ] = getCosts( result, lvqName )

runs = length(result.results);
costs = [];

for runIdx = 1 : runs
    
    runResult = result.results{runIdx,1};
    model = modelFinder(runResult, lvqName);
    if runIdx > 1 && size(costs,2) ~= size(model.costs,2)
        costs = nan;
        AVGcosts = nan;
        return;
    end
    costs = [costs;model.costs];
end

AVGcosts = mean(costs);

end

