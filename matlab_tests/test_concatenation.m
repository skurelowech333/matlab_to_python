% Test array concatenation
function [C, D] = test_concatenation()
    A = [1, 2, 3];
    B = [4, 5, 6];
    C = [A, B];
    D = [A; B];
end
