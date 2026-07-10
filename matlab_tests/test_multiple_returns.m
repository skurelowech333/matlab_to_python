% Test multiple return values
function [max_val, min_val, mean_val] = test_multiple_returns(data)
    max_val = max(data);
    min_val = min(data);
    mean_val = mean(data);
end
