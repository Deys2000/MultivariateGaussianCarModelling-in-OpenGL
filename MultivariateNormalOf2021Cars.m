% gather 18 columns of dimensions (excluding samples with NaN values)
data = load('2021CarsDimensions.mat');
% using simpler variables
A1 = data.A1; B1 = data.B1; C1 = data.C1;
%CW = data.CW;
D1 = data.D1; E1 = data.E1;
F1 = data.F1; G1 = data.G1; OH = data.OH;
OL = data.OL; OW = data.OW; TWF = data.TWF;
TWR = data.TWR; WB = data.WB;
% creating a matrix of values [dimensions by # of samples ]
dataTable = [A1';B1';C1';D1';E1';F1';G1';OH';OL';OW';TWF';TWR';WB'];
% defining parameters mu and Sigma
mu = mean(dataTable,2);
Sigma = cov(dataTable');


samplingPoints = 1;
%rng('default')
X = mvnrnd(mu,Sigma,samplingPoints);
save('ModellingData.mat', 'X')

%x =[130,175,40,88,119,93,107,169,508,192,163,164,307];%a point at high pdf
%X =[Xa;x];

%pdf = mvnpdf(X,mu',Sigma);

%clf

%corrplot(Sigma);

%% creating a plot of pdf's at a range of values

%scatter(1:size(pdf),pdf,'filled');
% histogram(pdf*10^20);
% xlabel('Dtrisibution Index');
% ylabel('Probability Density at sample');

%%
%for i = 1:36
%    subplot(6,6,i);
%    carPlotter(X(i,:,:));
%    title("PDF Value: " + pdf(i)*10^21 + " *10^{(-21)}");
%end


