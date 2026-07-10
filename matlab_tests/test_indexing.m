% Test array indexing and slicing
function test_indexing()
    A = [1, 2, 3, 4, 5; 6, 7, 8, 9, 10; 11, 12, 13, 14, 15];
    a = A(1, 1);
    b = A(2, 3);
    row = A(1, :);
    col = A(:, 2);
    submatrix = A(1:2, 2:4);
end
