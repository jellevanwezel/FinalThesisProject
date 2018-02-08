function [ cellArray ] = fn_exp_struct_to_input_cell( structure )
fieldsNames = fieldnames(structure);
cellArray = cell(1,length(fieldsNames) * 2);
for i = 1 : length(fieldsNames)
    name =  fieldsNames{i};
    value = getfield(structure,name);
    cellArray{1,i*2-1} = name;
    cellArray{1,i*2} = value;
end
end

