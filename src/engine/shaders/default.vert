#version 330 core

in vec3 in_position;
in vec3 in_color;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_proj;

out vec3 v_color;

void main() {
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    v_color = in_color;
}
