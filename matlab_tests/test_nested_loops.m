% Test nested loops
function matrix_sum = test_nested_loops(n, m)
    matrix_sum = 0;
    for i = 1:n
        for j = 1:m
            matrix_sum = matrix_sum + i * j;
        end
    end
end
