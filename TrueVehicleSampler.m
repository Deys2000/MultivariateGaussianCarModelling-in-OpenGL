data = load('2021CarsDimensions.mat');
RandomRow = randi(size(data,1));
RowValues = data(RandomRow, :);
