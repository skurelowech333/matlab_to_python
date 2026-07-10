% Test Cholesky decomposition
function L = test_cholesky()
    A = [4, 2; 2, 3];
    L = chol(A);
end
