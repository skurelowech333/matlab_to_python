% Test SVD (Singular Value Decomposition)
function [U, S, V] = test_svd()
    A = [1, 2; 3, 4; 5, 6];
    [U, S, V] = svd(A);
end
