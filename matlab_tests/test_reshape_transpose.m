% Test reshape and transpose
function test_reshape_transpose()
    A = [1, 2, 3, 4, 5, 6];
    B = reshape(A, 2, 3);
    C = reshape(A, 3, 2);
    D = transpose(B);
    E = B';
end
