% Test matrix norms
function test_matrix_norms()
    A = [3, 4];
    norm2 = norm(A);
    norm1 = norm(A, 1);
    norm_inf = norm(A, inf);
end
