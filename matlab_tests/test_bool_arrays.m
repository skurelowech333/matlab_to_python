% Test boolean arrays
function test_bool_arrays()
    A = [1, 2, 3; 4, 5, 6];
    mask = A > 3;
    selected = A(mask);
end
