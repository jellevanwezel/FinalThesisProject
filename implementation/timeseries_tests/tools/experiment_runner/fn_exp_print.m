function [ ] = fn_exp_print( exps )

for i = 1:size(exps,2)

    exp = exps{i};

    str = [exp.dataset,'-',exp.function,'-('];
    commaChar = '';
    for j = 1:size(exp.metaParams,2)
        if j ~= 1
            commaChar = ',';
        end
        str = strcat(str,commaChar,num2str(exp.metaParams{j}));
    end
    str = strcat(str,')');
    disp(str);
end
end
