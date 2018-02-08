%load('/home/jelle/RUG/FTP/data/pipe_segment_voltages/segments_with_type.mat');

figure;
hold on;



for i = 1:1:length(segments)

    segment = segments(i);
    years = segment.years;
    months = segment.months;
    volts = segment.v;
    id = segment.id;
    mtype = segment.type;
    
    firstV = volts(1);
    volts = firstV - volts;
    
    c='r';
    
    if mtype==9;c='b';end;
    if max(volts) < 5000
%         
%         for j = 1 : length(volts)
%             if abs(volts(j)) >= 1000
%                 volts = volts / 10;
%             end
%         end
        
        scatter(years + ((months-1)/12) ,volts,'.');
        
    end

end

plot([1987,2017],[0,0],'LineWidth',2,'color','k');