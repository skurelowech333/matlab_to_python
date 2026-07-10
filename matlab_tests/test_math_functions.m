% Test mathematical functions
function results = test_math_functions(x)
    results = zeros(1, 10);
    results(1) = sin(x);
    results(2) = cos(x);
    results(3) = tan(x);
    results(4) = sqrt(abs(x));
    results(5) = exp(x);
    results(6) = log(abs(x) + 1);
    results(7) = floor(x);
    results(8) = ceil(x);
    results(9) = round(x);
    results(10) = abs(x);
end
