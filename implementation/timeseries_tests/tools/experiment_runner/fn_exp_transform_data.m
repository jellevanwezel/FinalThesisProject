function [ data ] = fn_exp_transform_data( data, M )

for i = 1 : size(data,1)
    row = data(i,:);
    row = M * row';
    data(i,:) = row;
end


end

