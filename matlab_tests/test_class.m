classdef TestSatellite

    properties
        mass
        area
        name
    end


    methods

        % Constructor
        function obj = TestSatellite(m, a, n)

            obj.mass = m;
            obj.area = a;
            obj.name = n;

        end


        % Simple getter
        function m = getMass(obj)

            m = obj.mass;

        end


        % Compute ballistic coefficient
        function beta = ballisticCoefficient(obj)

            beta = obj.mass / obj.area;

        end


        % Update mass
        function obj = updateMass(obj, dm)

            obj.mass = obj.mass + dm;

        end

    end

end