%load('data/inlineSkate.mat');
%timeData = InlineSkate(1,1:end-1);
timeData = a(1:1000,3)';

bins = 17;
featureSize = 25;
featureData = nan(size(timeData,2)-featureSize-1,featureSize);
labels = nan(size(timeData,2)-featureSize -1,1);

for i = 1:(size(timeData,2)-featureSize-1)
    startLoc = i;
    endLoc = i+featureSize -1;
    featureData(i,:) = timeData(startLoc:endLoc);
    labels(i) = timeData(endLoc + 1);
end

tmax = max(timeData);
tmin = min(timeData);

for i = 1:size(labels,1)
    label = labels(i);
    label = ceil((label - tmin) / (tmax-tmin) * bins);
    labels(i) = label;
end
data = featureData;




