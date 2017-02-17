local t = {
% for sheet in excel:
    ${sheet.name} = {
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