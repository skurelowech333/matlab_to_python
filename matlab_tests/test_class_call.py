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


        % Getter
        function m = getMass(obj)

            m = obj.mass;

        end


        % Ballistic coefficient
        function beta = ballisticCoefficient(obj)

            beta = obj.mass / obj.area;

        end

    end

end


% =====================================================
% Test class usage
% =====================================================

sat = TestSatellite(1000, 20, "TestSat");


mass_value = sat.getMass();


beta_value = sat.ballisticCoefficient();


disp(mass_value)
disp(beta_value)