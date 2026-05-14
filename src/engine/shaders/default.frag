#version 330 core
in vec3 v_color;
in vec3 v_normal;
in vec3 v_fragpos;
uniform vec3 light_pos;
out vec4 fragColor;
void main() {
    float ambient = 0.3;
    vec3 norm = normalize(v_normal);
    vec3 lightdir = normalize(light_pos - v_fragpos);
    float diffuse = max(dot(norm, lightdir), 0.0);
    vec3 result = (ambient + diffuse) * v_color;
    fragColor = vec4(result, 1.0);
}
