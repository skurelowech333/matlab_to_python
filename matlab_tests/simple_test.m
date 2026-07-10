function y = simple_test(x)

% Basic arithmetic
a = x^2;
b = sqrt(a);

% MATLAB built-in conversion test
c = sin(x);

% Loop test
total = 0;

for i = 1:5
    total = total + i;
end

% Final output
y = b + c + total;

end