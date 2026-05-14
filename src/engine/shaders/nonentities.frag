#version 330 core
precision highp float;
in vec3 v_color;
in vec3 v_normal;
in vec3 v_fragpos;

uniform vec3 light_pos;

out vec4 fragColor;

void main() {
    // for nonentities
    vec3 norm = normalize(v_normal);
    vec3 lightdir = normalize(light_pos - v_fragpos);

    float diff = max(dot(norm, lightdir), 0.0) * 0.6;
    float ambient = 0.4;

    vec3 glow = vec3(0.04, 0.0, 0.0);
    vec3 result = (ambient + diff) * v_color + glow;

    fragColor = vec4(result, 1.0);
}
