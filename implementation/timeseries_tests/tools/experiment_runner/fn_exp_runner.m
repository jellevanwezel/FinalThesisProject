function [ results ] = fn_exp_runner(experiments)

results = cell(size(experiments,1),1);
pbarCount = 0;

for expIdx = 1 : size(experiments,2)
    experiment = experiments{1,expIdx};
    pbarCount =  pbarCount + experiment.runs; 
end

%todo make the thread pool  configurable

poolobj = gcp('nocreate');
if(isempty(poolobj))
    parpool('local',4);
end

disp('Experiments Started!');
disp(['Running ', num2str(size(experiments,2)), ' experiments.']);
disp(['Total of ', num2str(pbarCount), ' runs.']);

pbar = ProgressBar(pbarCount);
%parfor expIdx = 1 : size(experiments,2)
for expIdx = 1 : size(experiments,2)
    experiment = experiments{1,expIdx};

    funName = experiment.function;
    exp_fun = str2func(funName);
    experiment.results = cell(experiment.runs,1);

    for run = 1:experiment.runs
        dataset = experiment.dataSplits{run};
        params = [{dataset},experiment.params]; 
        try
            runResults = exp_fun(params{:});
        catch EM
            disp(EM.message);
            runResults = EM;
        end
        experiment.results{run} = runResults;
        pbar.progress;
    end

    experiment.date = datestr(datetime());
    results{expIdx} = experiment;

end

pbar.stop;
disp('Done!');

end

