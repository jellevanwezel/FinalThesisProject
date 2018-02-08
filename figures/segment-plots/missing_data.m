%==========================================================================
% Shows a barplot with the percentage of missing values for that year
% proportional to the amount of pipesegments that were active in that year.
%==========================================================================

clear;

load('/home/jelle/RUG/FTP/data/pipe_segment_voltages/segments_with_type.mat');

yearStruct = struct();
activeSegmentsPerYear = struct();

minYear = inf;
maxYear = -inf;

for i = 1:length(segments)

    segment = segments(i);
    years = unique(segment.years);
    volts = segment.v;
    id = segment.id;
    mtype = segment.material_type;
    
    localMinYear = min(years);
    localMaxYear = max(years);
    
    for j = localMinYear:localMaxYear
        hash = ['y',num2str(j)];
        if ~isfield(activeSegmentsPerYear,hash)
            activeSegmentsPerYear = setfield(activeSegmentsPerYear,hash,1);
            continue;
        end
        amount = getfield(activeSegmentsPerYear,hash)+1;
        activeSegmentsPerYear = setfield(activeSegmentsPerYear,hash,amount);
    end
    
    
    for j = 1:length(years)
        if minYear > years(j);minYear = years(j);end;
        if maxYear < years(j);maxYear = years(j);end;
        hash = ['y',num2str(years(j))];
        if ~isfield(yearStruct,hash)
            yearStruct = setfield(yearStruct,hash,1);
            continue;
        end
        amount = getfield(yearStruct,hash)+1;
        yearStruct = setfield(yearStruct,hash,amount);
    end
end

yearLabels = minYear:maxYear;
missingValues = nan(length(yearLabels),1);

for i = minYear:maxYear
    hash = ['y',num2str(i)];
    if ~isfield(yearStruct,hash)
            yearStruct = setfield(yearStruct,hash,0);
    end
    missingValues(i-minYear+1) = 1 - (getfield(yearStruct,hash)/getfield(activeSegmentsPerYear,hash));
end

nSegments = length(segments);
close all
f = figure;
bar(yearLabels,missingValues);
xlim([minYear, maxYear]);





