function [ g, epsilon ] = suvrelOD( data,labels, gamma)
%Suvrel Finds the weights of the features in the data
%   data - the data points
%   labels - the labels indexed by its data points
%   gamma - the ratio between inner and outer classes (default 2)
%   norm - normalisation (default unity)


%The number of classes
K = size(unique(labels),1);
%The amount of features
features = size(data,2);
%Gamma
gamma = 2/(K-1);

epsilon = zeros(features);

%Initial matrix for the mean of the classes
for u = 1: features;
    for v = 1: features;
        
       if u ~= v
           continue;
       end
       
       featureClassMeansu = zeros(K,1);
       featureClassMeansv = zeros(K,1);
        
        covVal = 0;
        for a  = unique(labels)';
            classData = data(labels==a,:);
            covMatrix = cov(classData(:,u),classData(:,v),1);
            covVal = covVal + covMatrix(1,2); % xy
            
            featureClassMeansu(a,1) = mean(classData(:,u));
            featureClassMeansv(a,1) = mean(classData(:,v));
        end
       
        covMeans = 1/K * sum(featureClassMeansu .* featureClassMeansv) - (1/K .* sum(featureClassMeansu)) * (1/K .* sum(featureClassMeansv));
        
        %covMeansMatrix = cov(featureClassMeansu,featureClassMeansv,1);
        %covMeans = covMeansMatrix(1,2);
        
        epsilon(u,v) = (2-(K-1)*gamma)*covVal - gamma*(K^2)*covMeans;
    end
end

g = -epsilon ./ sqrt(sum(epsilon(:).^2));

end