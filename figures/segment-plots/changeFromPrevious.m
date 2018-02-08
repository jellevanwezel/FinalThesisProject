load('/home/jelle/RUG/FTP/data/pipe_segment_voltages/segments_with_type.mat');

figure;
hold on;

for i = 1:1:length(segments)

    segment = segments(i);
    years = segment.years;
    volts = segment.v;
    id = segment.id;
    mtype = segment.material_type;
    
    firstV = volts(1);
    dvolts = nan(length(volts)-1,1);
    for j = 2:length(volts)
        dvolts(j) = abs(volts(j-1)-volts(j)); 
    end
    c='r';
    if mtype==9;c='b';end;
    if max(dvolts) < 5000
        plot(years(2:end) - min(years(2:end)),dvolts(2:end),'color',c);
    end

end

plot((1:31)-1,zeros(31,1),'LineWidth',4,'color','k');