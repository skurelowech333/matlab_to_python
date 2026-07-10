% Test control flow with for loops
function sum_result = test_for_loop(n)
    sum_result = 0;
    for i = 1:n
        sum_result = sum_result + i;
    end
end
