samplingPoints = 1;
load('Mu_and_Sigma.mat', 'mu')
load('Mu_and_Sigma.mat', 'Sigma')

rng('shuffle') % changes the random generator seed
X = mvnrnd(mu,Sigma,samplingPoints);
save('ModellingData.mat', 'X')



