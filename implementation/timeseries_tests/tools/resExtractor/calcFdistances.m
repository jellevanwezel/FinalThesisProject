function [ distances ] = calcFdistances( As, Bs )
distances = nan(1,max([length(As),length(Bs)]));
if(length(As) > 1)
    for matIdx = 1 : length(As)
        A = As{1,matIdx};
        B = Bs{1,matIdx};
        distances(1,matIdx) = calcFdistance(A,B);
    end
    return;
end
A = As{1,1};

for matIdx = 1 : length(Bs)
    B = Bs{1,matIdx};
    distances(1,matIdx) = calcFdistance(A,B);
end
end

