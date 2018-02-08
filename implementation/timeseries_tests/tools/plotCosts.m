method = 'gmlvq';

for i = 1:length(resultTable)
    s = resultTable(i);
    if(length(s.method) == length(method) && all(s.method == method))
        figure;
        title([s.dataset,' - ',s.pre]);
        hold on;
%         for j = 1:10
%             plot(s.costs{j,1});
%         end
        avgCosts = zeros(1,1001);
        for j = 1:10
              pavgCosts = avgCosts + s.costs{j,1};
        end
        plot(pavgCosts/10);
        hold off;
    end
end