#version 330 core
in vec3 in_position;
uniform mat4 m_proj;
uniform mat4 m_view;
out vec3 v_direction;
void main() {
    v_direction = in_position;
    mat4 view_no_translate = mat4(mat3(m_view));
    vec4 pos = m_proj * view_no_translate * vec4(in_position, 1.0);
    gl_Position = pos.xyww;
}
