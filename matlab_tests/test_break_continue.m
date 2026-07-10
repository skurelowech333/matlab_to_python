% Test break and continue
function result = test_break_continue(limit)
    result = 0;
    for i = 1:limit
        if i == 5
            continue;
        end
        if i == 10
            break;
        end
        result = result + i;
    end
end
