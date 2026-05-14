#version 330 core
in vec3 in_position;
in vec3 in_color;
in vec3 in_normal;
uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_proj;
out vec3 v_color;
out vec3 v_normal;
out vec3 v_fragpos;
void main() {
    vec4 worldpos = m_model * vec4(in_position, 1.0);
    gl_Position = m_proj * m_view * worldpos;
    v_fragpos = worldpos.xyz;
    v_normal = mat3(transpose(inverse(m_model))) * in_normal;
    v_color = in_color;
}
