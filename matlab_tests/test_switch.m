% Test switch-case statements
function operation = test_switch(choice)
    switch choice
        case 1
            operation = 'addition';
        case 2
            operation = 'subtraction';
        case 3
            operation = 'multiplication';
        case 4
            operation = 'division';
        otherwise
            operation = 'unknown';
    end
end
