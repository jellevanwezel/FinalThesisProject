dataPath = '/home/jelle/RUG/FTP/figures/interpolation-cross-validation/data/';
figurePath = '/home/jelle/RUG/FTP/figures/interpolation-cross-validation/figures/';
imageName = 'Average-LOOCV-Error';

%Get data to plot

n = 50;
areaNames = {  'Almelo Castello.csv',...
				'De Krim.csv',...
				'Enter.csv',...
				...%'Oldenzaal.csv', %Has no measurments
				'Vriezenveen.csv',...
				'Almelo De Pook.csv',...
				'Delden.csv',...
				'Goor.csv',...
				'Vroomshoop.csv',...
				'Almelo Ten Cate.csv',...
				'Denekamp 2.csv',...
				'Hardenberg.csv',...
				'Rossum.csv',...
				'Wierden.csv',...
				'Almelo Tusveld.csv',...
				'Denekamp.csv',...
				'Hengelvelde.csv',...
				'Slagharen.csv',...
				'Almelo Windmolenbroek.csv',...
				'Deurningen.csv',...
				'Markelo.csv',...
				'Tubbergen.csv'
                };
avgError = zeros(1,n);
for i = 1:length(areaNames)
    data = csvread([dataPath,areaNames{i}]);
    avgError = avgError + mean(data);
end
avgError = avgError ./ length(areaNames);


%Create figure

close all;
set(0,'defaultTextInterpreter','latex');
figure1 = figure('visible','off');

% Create axes
axes1 = axes('Parent',figure1);
box(axes1,'on');
hold(axes1,'on');

% Create plot
plot(avgError,'DisplayName','LOOCV Error','LineWidth',5);

% Create xlabel
xlabel('$N_{coefs}$');

% Create ylabel
ylabel('Average LOOCV Error');

set(gca,'TickLabelInterpreter', 'latex','fontsize',20);

saveas(gca,[figurePath,imageName,'.pdf']);
system(['pdfcrop ',figurePath,imageName,'.pdf ',figurePath,imageName,'.pdf']);