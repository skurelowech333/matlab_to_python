% Test for loop with a step value
function result = test_for_step(n)
    result = 0;
    for i = 1:2:n
        result = result + i;
    end
end
