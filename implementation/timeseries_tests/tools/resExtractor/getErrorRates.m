function [ train, test ] = getErrorRates( result , methodName)

train = nan(1,length(result.results));
test = nan(1,length(result.results));

for runIdx = 1 : length(result.results)
    
    runResult = result.results{runIdx,1};
    if isfield(runResult, methodName);runResult = getfield(runResult,methodName);end;
    train(1,runIdx) = runResult.trainError(1,end);
    test(1,runIdx) = runResult.testError(1,end);
    
end
train = [mean(train),std(train)];
test = [mean(test),std(test)];
end

