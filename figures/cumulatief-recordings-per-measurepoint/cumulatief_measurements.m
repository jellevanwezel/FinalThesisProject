imageName = 'cumulatief-recordings-per-measurepoint';
path = '/home/jelle/RUG/FTP/figures/cumulatief-recordings-per-measurepoint/';
load([path,'recordings_per_measurepoint.mat']);

histData = histc(amount,unique(amount));
cumulatiefData = nan(length(histData),1);
for i = 1:length(histData);
    cumulatiefData(i) = sum(histData(i:end,1));
end;


close all;
set(0,'defaultTextInterpreter','latex');
figure1 = figure('visible','off');

% Create axes
axes1 = axes('Parent',figure1);
box(axes1,'on');
hold(axes1,'on');

% Create plot
plot(cumulatiefData,'DisplayName','Measuring Points','LineWidth',5);

% Create xlabel
xlabel('Recordings per Measuring Point');

% Create ylabel
ylabel('Cumulatief amount of measure points');

set(gca,'TickLabelInterpreter', 'latex','fontsize',20);

saveas(gca,[path,imageName,'.pdf']);
system(['pdfcrop ',path,imageName,'.pdf ',path,imageName,'.pdf']);

