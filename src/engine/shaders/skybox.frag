#version 330 core
in vec3 v_direction;
uniform vec3 sky_top;
uniform vec3 sky_bottom;
out vec4 fragColor;
void main() {
    float t = clamp(normalize(v_direction).y * + 0.8, 0.0, 1.0);
    fragColor = vec4(mix(sky_bottom, sky_top, t), 1.0);
}
