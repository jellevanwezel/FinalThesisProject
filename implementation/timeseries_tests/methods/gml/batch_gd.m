function [ W, energies ] = batch_gd(W, data,S,D, eta, maxIter)

%figure;
%hold on;

%h = animatedline;

a = 0.9;
energies = nan(ceil(maxIter/100),1);

for t = 1:maxIter
    W = W - eta * gradient(S,D,W,data,a);
    energies(t) = energy(data,S,D,a,W);
    %addpoints(h,t,energies(t));
    %drawnow;
end

end