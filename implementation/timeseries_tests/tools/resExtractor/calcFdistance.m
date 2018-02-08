function [ d ] = calcFdistance( A,B )

if (size(A,1)) ~= (size(A,2)); A = diag(A);end;
if (size(B,1)) ~= (size(B,2)); B = diag(B);end;

A = A / trace(A);
B = B / trace(B);
fnormA = norm(A'*A,'fro');
fnormB = norm(B'*B,'fro');
d = abs(fnormA - fnormB);
end

