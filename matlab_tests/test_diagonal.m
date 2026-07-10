% Test matrix diagonal extraction
function test_diagonal()
    A = [1, 2, 3; 4, 5, 6; 7, 8, 9];
    d = diag(A);
    D = diag(d);
end
