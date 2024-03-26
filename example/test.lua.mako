local t = {
% for name, sheet in excel.items():
    ${name} = {
    % for row in sheet:
        {
        % for key in row:
            ${key} = ${format(row[key])},
        % endfor
        },
    % endfor
    }
}
return t
% endfor
