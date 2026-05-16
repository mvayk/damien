#version 330

in vec2 in_position;
in vec2 in_uv;
out vec2 v_uv;

uniform vec2 screen_size;

void main() {
    vec2 ndc = (in_position / screen_size) * 2.0 - 1.0;
    //ndc.y = -ndc.y; doesnt need to be flipped
    gl_Position = vec4(ndc, 0.0, 1.0);
    v_uv = in_uv;
}
