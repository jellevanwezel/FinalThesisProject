clear;

load('/home/jelle/RUG/FTP/data/pipe_segment_voltages/segments_with_type.mat');

mpy = cell(1,40);
for i = 1:length(segments)

    segment = segments(i);
    years = segment.years;
    volts = segment.v;
    id = segment.id;
    mtype = segment.material_type;
    
    for j = 1:length(years)
        y = years(j) - min(years) + 1;
        yearVals = mpy{y};
        if(volts(j) > -10000)
            yearVals = [yearVals,volts(j)];
            mpy(y) = {yearVals};
        end
    end
    
end

averages = zeros(size(mpy,2),1);

for i = 1:size(mpy,2)
    yearVals = mpy{i};
    averages(i) = mean(yearVals);
end

plot(averages);