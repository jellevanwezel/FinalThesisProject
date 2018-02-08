clear;
close all;

dataSet = 'iris';
stochMaxItr = 100000;
stochStepSize = 0.001; %difined in the ADAM paper
batchMaxItr = 500;
batchStepSize = 0.001; %difined in the ADAM paper


load(strcat('/home/jelle/RUG/RI/',dataSet,'/D.mat'));
load(strcat('/home/jelle/RUG/RI/',dataSet,'/S.mat'));
load(strcat('/home/jelle/RUG/RI/',dataSet,'/',dataSet,'.mat'));
load(strcat('/home/jelle/RUG/RI/',dataSet,'/suvrel-weights.mat'));

[~,stochEnergiesEYE] = sgd2(eye(size(data,2)),data,S,D,stochStepSize,stochMaxItr);
[~,stochEnergiesSUV] = sgd2(diag(weights),data,S,D,stochStepSize,stochMaxItr);
[~,stochEnergiesCOV] = sgd2(cov(data),data,S,D,stochStepSize,stochMaxItr);

[~,batchEnergiesEYE] = batch_gd(eye(size(data,2)),data,S,D,batchStepSize,batchMaxItr);
[~,batchEnergiesSUV] = batch_gd(diag(weights),data,S,D,batchStepSize,batchMaxItr);
[~,batchEnergiesCOV] = batch_gd(cov(data),data,S,D,batchStepSize,batchMaxItr);

figure;
hold on;

title('Stochastic gradient descent');
xlabel('t');
ylabel('E');

plot(1:size(stochEnergiesEYE,1),stochEnergiesEYE);
plot(1:size(stochEnergiesSUV,1),stochEnergiesSUV);
plot(1:size(stochEnergiesCOV,1),stochEnergiesCOV);

hold off;

figure;
hold on;

title('Batch gradient descent')
xlabel('t');
ylabel('E')

plot(1:size(batchEnergiesEYE,1),batchEnergiesEYE);
plot(1:size(batchEnergiesSUV,1),batchEnergiesSUV);
plot(1:size(batchEnergiesCOV,1),batchEnergiesCOV);