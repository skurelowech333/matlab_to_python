% Test matrix multiplication vs element-wise
function test_multiplication_types()
    A = [1, 2; 3, 4];
    B = [5, 6; 7, 8];
    matrix_mult = A * B;
    element_mult = A .* B;
end
