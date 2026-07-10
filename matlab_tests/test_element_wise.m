% Test element-wise operations
function test_element_wise()
    A = [1, 2, 3; 4, 5, 6];
    B = [2, 3, 4; 5, 6, 7];
    C = A .* B;
    D = A ./ B;
    E = A .^ 2;
    F = A + B;
    G = A - B;
end
