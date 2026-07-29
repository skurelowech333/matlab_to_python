% Test basic cell array creation and indexing
function out = test_cell_arrays()
    % Create a simple cell array of numbers
    c = {1, 2, 3};
    
    % Modify a middle element
    c{2} = 10;
    
    % Read out and combine values
    out = c{1} + c{2} + c{3};  % 1 + 10 + 3 = 14
end