% Test multiple function calls in expression
function result = test_multiple_calls(a, b, c)
    result = max(a, max(b, c)) + min(a, min(b, c));
end
