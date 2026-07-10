% Test eigenvalue decomposition
function [eigenvalues, eigenvectors] = test_eigenvalues()
    A = [1, 2; 2, 3];
    [eigenvectors, eigenvalues] = eig(A);
end
