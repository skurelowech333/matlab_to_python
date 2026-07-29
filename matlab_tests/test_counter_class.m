classdef Counter
    properties
        Value
    end

    methods
        function obj = Counter(initial)
            if nargin < 1
                initial = 0;
            end
            obj.Value = initial;
        end

        function obj = increment(obj, amount)
            if nargin < 2
                amount = 1;
            end
            obj.Value = obj.Value + amount;
        end

        function v = getValue(obj)
            v = obj.Value;
        end
    end
end