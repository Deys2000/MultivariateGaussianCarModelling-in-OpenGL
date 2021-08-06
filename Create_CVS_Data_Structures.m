% load the file with all name parameters as well
CVS = readtable('spe2021.csv');

%remove unnecessary columns
CVS = removevars( CVS, {'MYR', 'WB', 'CW', 'WDIST'} );

% remove missing rows of information
CVS = rmmissing(CVS);

% Save Information to be processed later
save('2021CarsDimensions.mat', 'CVS');


