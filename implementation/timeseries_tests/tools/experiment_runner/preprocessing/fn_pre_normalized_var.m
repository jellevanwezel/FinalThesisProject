function [ data ] = fn_pre_normalized_var( data )
%FN_PRE_NORMALIZED_VAR Summary of this function goes here
%   Detailed explanation goes here
data = bsxfun(@rdivide,data,std(data,1,1));

end

