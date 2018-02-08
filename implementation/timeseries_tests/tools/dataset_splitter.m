bestResults = struct();

for i = 1 : length(resultTable)
    %find per dataset per method list the 'best'
    s = resultTable(i);
    
    if isfield(bestResults, [s.dataset(1:4),'_',s.method])
       r = getfield(bestResults,[s.dataset(1:4),'_',s.method]);
       if r.testAVG > s.testAVG
           bestResults = setfield(bestResults,[s.dataset(1:4),'_',s.method],s);
       end
       continue;
    end
    bestResults = setfield(bestResults,[s.dataset(1:4),'_',s.method],s);
end

names = fieldnames(bestResults);
bestResultsAsArray = getfield(bestResults,names{1});
for i = 2 : length(names)
    bestResultsAsArray(i) = getfield(bestResults,names{i});
end