% Test try-catch error handling
function result = test_try_catch(a, b)
    try
        result = a / b;
    catch
        result = 0;
    end
end
