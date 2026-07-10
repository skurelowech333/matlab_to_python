% Test if-elseif-else statements
function category = test_conditional(value)
    if value < 0
        category = 'negative';
    elseif value == 0
        category = 'zero';
    elseif value < 10
        category = 'small';
    else
        category = 'large';
    end
end
