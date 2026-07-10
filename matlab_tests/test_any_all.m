% Test any and all
function test_any_all()
    A = [true, false, true];
    B = [true, true, true];
    result1 = any(A);
    result2 = all(A);
    result3 = any(B);
    result4 = all(B);
end
