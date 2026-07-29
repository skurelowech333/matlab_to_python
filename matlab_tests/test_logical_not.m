% Test logical NOT operator (~)
function result = test_logical_not(x)
    if ~(x > 5)
        result = 1;
    else
        result = 0;
    end
end
