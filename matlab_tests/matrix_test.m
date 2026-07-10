function y = matrix_test(x)

% Matrix creation
A = [1 2;
     3 4];

% Matrix multiply
B = A .* A;

% Inverse
C = inv(A);

y = C*x;

end