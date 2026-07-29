classdef Point
    % Simple 2D point class to exercise:
    %  - Multiple properties
    %  - Constructor with two arguments
    %  - Methods that mutate obj
    %  - Methods that return scalar and logical values

    properties
        X
        Y
    end

    methods
        function obj = Point(x, y)
            % Constructor: initialize properties
            obj.X = x;
            obj.Y = y;
        end

        function obj = move(obj, dx, dy)
            % Translate the point by (dx, dy)
            obj.X = obj.X + dx;
            obj.Y = obj.Y + dy;
        end

        function d = distanceToOrigin(obj)
            % Return Euclidean distance from origin
            d = sqrt(obj.X^2 + obj.Y^2);
        end

        function isAbove = isAboveXAxis(obj)
            % Return true if the point is above the x‑axis
            isAbove = (obj.Y > 0);
        end

        function isRight = isRightOfYAxis(obj)
            % Return true if the point is right of the y‑axis
            isRight = (obj.X > 0);
        end
    end
end