% Test matrix algebra
function test_matrix_algebra()
    A = [1, 2; 3, 4];
    det_A = det(A);
    inv_A = inv(A);
    trace_A = trace(A);
    rank_A = rank(A);
end
