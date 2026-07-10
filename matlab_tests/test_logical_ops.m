% Test logical operations
function result = test_logical_ops(a, b, c)
    result1 = (a > 5) && (b < 10);
    result2 = (c == 0) || (a > b);
    result3 = ~(a == b);
    if result1 && result2 && ~result3
        result = 1;
    else
        result = 0;
    end
end
