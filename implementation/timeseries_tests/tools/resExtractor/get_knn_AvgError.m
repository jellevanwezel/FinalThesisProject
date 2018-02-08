function [ avgError,k ] = get_knn_AvgError( result )

errors = nan(25,length(result.results));

for runIdx = 1 : length(result.results)
    runResult = result.results{runIdx,1};
    errors(:,runIdx) = runResult.error;
end

[avgError,k] = min(mean(errors,2));
%stdError = std(errors,2);

end

