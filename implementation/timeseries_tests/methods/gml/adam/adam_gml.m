function [ minW, energies ] = adam_gml(W, data,labels,S,D, maxIter, stepSize)

% stepSize = 0.001
% beta1 = 0.9
% beta2 = 0.999
% epsilon = 10^(-8)


beta1 = 0.9;
beta2 = 0.999;
epsilon = 10^(-8);

a = 0.9;
energies = nan(maxIter,1);
minEnergy = inf;
minW = W;
m = zeros(size(W,2));
v = zeros(size(W,2));

for t = 1:maxIter
    s = S(randi(size(S,1)),:);
    % not magix, Da is the combinations with the same label in it as
    % selected from S
    Da = [D(labels(D(:,1)) == labels(s(1)),:) ; D(labels(D(:,2)) == labels(s(1)),:)];
    d = Da(randi(size(Da,1)),:);
    grad = gradient(s,d,W,data,a);
    %grad = gradient(S,D,W,data,a);
    m = beta1 * m + (1-beta1) * grad; 
    v = beta2 * v + (1-beta2) * grad.^2;
    mHat = m ./ (1-beta1^t);
    vHat = v ./ (1-beta2^t);
    W = W - stepSize * (mHat ./ (sqrt(vHat) + epsilon));
    energies(t) = energy(data,S,D,a,W);
    if energies(t) < minEnergy
        minW = W;
    end
end

end

