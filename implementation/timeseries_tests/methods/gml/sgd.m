function [ W, energies ] = sgd( n, data, labels, maxIter, bp, W)
a = 0.9;
dataSize = size(data,1);
batchSize = floor((dataSize / 100 * bp));
nfeatures = size(data,2);
lowestW = W;
lowestE = inf;
count = 0;

%W = eye(nfeatures);
%W = cov(data);

energies = nan(1,maxIter);

for i = 1:maxIter    
        
    % Get all permutations of the current batch.
    % Randomize the indexes to retrieve a group of random datapoints of size
    % batchSize. By randomizing the index we make sure we have the right
    % label for each data-point.
    perms = randperm(dataSize);
    miniData = data(perms(1,1:batchSize),:);
    miniLabels = labels(perms(1,1:batchSize));
    %Get all permutations of the current batch.
    indexes = 1:batchSize;
    permutations = nchoosek(indexes,2);
    %Get permutations of intraclass and interclass
    D = permutations(miniLabels(permutations(:,1)) ~= miniLabels(permutations(:,2)),:);
    S = permutations(miniLabels(permutations(:,1)) == miniLabels(permutations(:,2)),:);
    W = W ./ max(abs(W(:)));
    for k = 1 : nfeatures   
        wk = W(k,:)';
        eD = 0; %intraclass energy for bookkeeping
        eS = 0; %interclass energy for bookkeeping
        dwkD = 0; %delta wk D
        dwkS = 0; %delta wk S
        
        %Calculating sum of energy-gradient for interclasses
        for j = 1 : size(D,1)
            xi = miniData(D(j,1),:)';
            xj = miniData(D(j,2),:)';
            %dist = mDist(xi,xj,W);
            dist = norm(W*xi-W*xj);
            %dist = mahDist(xi,xj,W);           
            frac = (1 - min([dist;1])) / dist;
            dwkD = dwkD + frac * ((wk' * (xi-xj)) * (xi-xj));
            %energy
            if k == 1
                eD = eD + (1 - min([dist;1]))^2;
            end
        end    
        
        %Calculating sum of energy-gradient for intraclasses
        for j = 1 : size(S,1)          
            xi = miniData(S(j,1),:)';
            xj = miniData(S(j,2),:)';
            
            dwkS = dwkS + ((wk' * (xi-xj)) * (xi-xj));
            %energy
            if k == 1
                eS = eS +  norm(W*xi-W*xj)^2; %mDist(xi,xj,W)^2;
            end
        end
        
        
        %Calculating total gradient
        dwkD = dwkD * -2 * a;
        dwkS = dwkS * 2 * (1-a);
        dwk =  dwkD + dwkS;
        W(k,:) = (W(k,:)' - n * dwk)';
        if k == 1
            E = (eD * a) + (eS * (1-a));
        end
    end
    energies(1,i) = E;
    dlmwrite('energies.csv',E,'delimiter',',','-append');
    if(lowestE > E)
        lowestE = E;
        lowestW = W;
        csvwrite('w.csv',W);
        count = 0;
    else
        count = count+1;
    end
    
    if count > 1000
        W = lowestW;
        energies = energies(1,1:i);
        return;
    end

end

W = lowestW;

end
