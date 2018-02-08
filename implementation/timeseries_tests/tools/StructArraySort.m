function [ ASorted ] = StructArraySort( A, col )

Afields = fieldnames(A);
Acell = struct2cell(A);
sz = size(Acell);
Acell = reshape(Acell, sz(1), []);
Acell = Acell';
Acell = sortrows(Acell, col);
Acell = reshape(Acell', sz);
ASorted = cell2struct(Acell, Afields, 1);

end

