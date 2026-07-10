% Test inverse and determinant
function test_inv_det()
    A = [1, 2; 3, 5];
    A_inv = inv(A);
    det_A = det(A);
    A_times_inv = A * A_inv;
end
