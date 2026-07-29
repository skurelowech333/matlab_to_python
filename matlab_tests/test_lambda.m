% Test anonymous function (lambda) translation
function result = test_lambda(x)
    f = @(t) t * t + 1;
    result = f(x);
end
