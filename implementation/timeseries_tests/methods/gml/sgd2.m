function [ W, energies ] = sgd2(W, data,S,D, eta, maxIter)

%figure;
%hold on;

%h = animatedline;

a = 0.9;
energies = nan(ceil(maxIter/100),1);

for t = 1:maxIter
    s = S(randi(size(S,1)),:);
    d = D(randi(size(D,1)),:);
    W = W - eta * gradient(s,d,W,data,a);
    energies(t) = energy(data,S,D,a,W);
    %addpoints(h,t,energies(t));
    %drawnow;
end

end

