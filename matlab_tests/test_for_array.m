% Test for loop over a vector (array iteration)
function total = test_for_array(n)
    values = [1, 3, 5, 7, 9];
    total = 0;
    for v = values
        if v <= n
            total = total + v;
        end
    end
end
