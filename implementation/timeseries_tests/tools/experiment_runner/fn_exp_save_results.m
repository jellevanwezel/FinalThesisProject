function [ ] = fn_exp_save_results( results, resultsPath )

disp('Saving results.');

for i = 1 : size(results, 2)
   
    result = results{i};
    resultPath = [resultsPath, '/', result.dataSetName, '/', result.function(8:end), '/', result.preprocessing(8:end),'/'];
    [~, ~, ~] = mkdir(resultPath);
    
    fileName = ['results_', result.function(8:end),'_', result.date,'.mat'];
    save([resultPath, '/', fileName], 'result');
    
end

disp(['Results saved to: ', resultsPath]);

end

