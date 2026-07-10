% Test matrix operations
function matrix_test()
    A = [1, 2, 3; 4, 5, 6; 7, 8, 9];
    B = [1, 0, 0; 0, 1, 0; 0, 0, 1];
    C = A * B;
    D = A .* B;
    E = transpose(A);
    F = A';
end
