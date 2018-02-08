
startMpoint = 1;
endMpoint = nan;
bakV = v;
segments = [];
for i = 1 : length(v)    
    curMPoint = mPoint(i);
    if curMPoint ~= mPoint(startMpoint)
        endMpoint = i-1;
        curVolts = v(startMpoint:endMpoint);
        curYears = year(startMpoint:endMpoint);
        mtype = mtypes(startMpoint);
        segment = struct('id',mPoint(startMpoint), 'v',curVolts,'years',curYears,'material_type',mtype);
        segments = [segments,segment];
        %v(startMpoint:endMpoint) = (curVolts - min(curVolts)) ./ (max(curVolts) - min(curVolts));
        startMpoint = i;
    end
    if i == length(v)
        endMpoint = i;
        curVolts = v(startMpoint:endMpoint);
        curYears = year(startMpoint:endMpoint);
        mtype = mtypes(startMpoint);
        %v(startMpoint:endMpoint) = (curVolts - min(curVolts)) ./ (max(curVolts) - min(curVolts));
        segment = struct('id',mPoint(startMpoint), 'v',curVolts,'years',curYears,'material_type',mtype);
        segments = [segments,segment];
    end
end