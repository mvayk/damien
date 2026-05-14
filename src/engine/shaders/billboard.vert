#version 330 core
in vec3 in_position;
in vec2 in_texcoord;
uniform mat4 m_proj;
uniform mat4 m_view;
uniform vec3 enemy_pos;
uniform bool follow_camera;
out vec2 v_texcoord;
void main() {
    vec3 right = vec3(m_view[0][0], m_view[1][0], m_view[2][0]);
    vec3 up;
    if (follow_camera) {
        up = vec3(m_view[0][1], m_view[1][1], m_view[2][1]);
    } else {
        up = vec3(0.0, 1.0, 0.0);
    }
    vec3 world_pos = enemy_pos + right * in_position.x + up * in_position.y;
    gl_Position = m_proj * m_view * vec4(world_pos, 1.0);
    v_texcoord = in_texcoord;
}
