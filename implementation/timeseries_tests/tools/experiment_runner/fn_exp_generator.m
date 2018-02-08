function [ experiments ] = fn_exp_generator(funName, datasets, dataPath, preproc, runs, params)
pCombs = fn_exp_paramCombs(params);

combAmount = size(pCombs,1);
if combAmount == 0
    combAmount = 1;
end

expSize = combAmount * size(preproc,2) * size(datasets,2);
experiments = cell(1,expSize);
expCount = 0;

for datasetIdx = 1:size(datasets,2)
    dataSetName = datasets{datasetIdx};
    dataSetPath = [dataPath,'/',dataSetName,'/',dataSetName,'.mat'];
    load(dataSetPath,'data','labels');
    
    for preProsIdx = 1 : size(preproc,2)
        preProsFnName = ['fn_pre_',preproc{preProsIdx}];
        preProsFn = str2func(preProsFnName);
        preProsData = preProsFn(data);
        
        experiment = struct();
        experiment.dataSetName = dataSetName;
        experiment.function = ['fn_exp_',funName];
        experiment.preprocessing = preProsFnName;
        experiment.runs = runs;
        experiment.dataset = struct('data',preProsData,'labels',labels);
        experiment.dataSplits = cell(runs,1);

        for run = 1:runs
            experiment.dataSplits{run} = fn_pre_splitter(preProsData, labels, 0.1);
        end
        
        if size(pCombs,1) == 0
            expCount = expCount + 1;
            experiment.params = {};
            experiments{1,expCount} = experiment;
        end
        
        for paramIdx = 1:size(pCombs,1)
            expCount = expCount + 1;
            experiment.params = {pCombs{paramIdx,:}};
            experiments{1,expCount} = experiment;
        end
        
    end
end
end