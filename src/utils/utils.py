from pathlib import Path

import numpy as np


def load_file_contents(path):
    base = Path(__file__).parent.parent
    absolute = (base / path).resolve()

    return absolute.read_text(encoding="utf8")
    # return Path(path).read_text(encoding='utf8')


# glm replacement
def perspective(fov_deg, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov_deg) / 2)
    return np.array(
        [
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), -1],
            [0, 0, (2 * far * near) / (near - far), 0],
        ],
        dtype="f4",
    )


def look_at(eye, target, up):
    f = normalize(target - eye)  # forward
    r = normalize(np.cross(f, up))  # right
    u = np.cross(r, f)  # true up
    return np.array(
        [
            [r[0], u[0], -f[0], 0],
            [r[1], u[1], -f[1], 0],
            [r[2], u[2], -f[2], 0],
            [-np.dot(r, eye), -np.dot(u, eye), np.dot(f, eye), 1],
        ],
        dtype="f4",
    )


def normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def translate(x, y, z):
    m = np.eye(4, dtype="f4")
    m[3, :3] = [x, y, z]
    return m


def scale(x, y, z):
    return np.diag([x, y, z, 1]).astype("f4")


def rotate_x(deg):
    r = np.radians(deg)
    return np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(r), np.sin(r), 0],
            [0, -np.sin(r), np.cos(r), 0],
            [0, 0, 0, 1],
        ],
        dtype="f4",
    )


def rotate_y(deg):
    r = np.radians(deg)
    return np.array(
        [
            [np.cos(r), 0, np.sin(r), 0],
            [0, 1, 0, 0],
            [-np.sin(r), 0, np.cos(r), 0],
            [0, 0, 0, 1],
        ],
        dtype="f4",
    )


def rotate_z(deg):
    r = np.radians(deg)
    return np.array(
        [
            [np.cos(r), np.sin(r), 0, 0],
            [-np.sin(r), np.cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype="f4",
    )
