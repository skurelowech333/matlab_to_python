% Test array statistics
function stats = test_array_stats(data)
    stats = zeros(1, 5);
    stats(1) = sum(data);
    stats(2) = mean(data);
    stats(3) = max(data);
    stats(4) = min(data);
    stats(5) = std(data);
end
