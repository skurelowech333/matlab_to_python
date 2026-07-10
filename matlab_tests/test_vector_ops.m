% Test vector operations
function test_vector_ops()
    v1 = [1, 2, 3];
    v2 = [4, 5, 6];
    dot_product = dot(v1, v2);
    cross_product = cross(v1, v2);
    norm_v1 = norm(v1);
    normalized = v1 / norm(v1);
end
