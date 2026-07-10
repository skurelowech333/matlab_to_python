% Test QR decomposition
function [Q, R] = test_qr_decomposition()
    A = [1, 2; 3, 4; 5, 6];
    [Q, R] = qr(A);
end
