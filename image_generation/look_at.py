import numpy as np


def normalize(x: np.ndarray) -> np.ndarray:
    assert x.ndim == 1, 'x must be a vector (ndim: 1)'
    return x / np.linalg.norm(x)


def look_at(
    eye,
    target,
    up,
) -> np.ndarray:
    """Returns transformation matrix with eye, at and up.
    Parameters
    ----------
    eye: (3,) float
        Camera position.
    target: (3,) float
        Camera look_at position.
    up: (3,) float
        Vector that defines y-axis of camera (z-axis is vector from eye to at).
    Returns
    -------
    T_cam2world: (4, 4) float (if return_homography is True)
        Homography transformation matrix from camera to world.
        Points are transformed like below:
            # x: camera coordinate, y: world coordinate
            y = trimesh.transforms.transform_points(x, T_cam2world)
            x = trimesh.transforms.transform_points(
                y, np.linalg.inv(T_cam2world)
            )
    """
    eye = np.asarray(eye, dtype=float)

    if target is None:
        target = np.array([0, 0, 0], dtype=float)
    else:
        target = np.asarray(target, dtype=float)

    if up is None:
        up = np.array([0, 0, -1], dtype=float)
    else:
        up = np.asarray(up, dtype=float)

    assert eye.shape == (3,), 'eye must be (3,) float'
    assert target.shape == (3,), 'target must be (3,) float'
    assert up.shape == (3,), 'up must be (3,) float'

    # create new axes
    z_axis = normalize(target - eye)
    x_axis = normalize(np.cross(up, z_axis))
    y_axis = normalize(np.cross(z_axis, x_axis))

    # create rotation matrix: [bs, 3, 3]
    R = np.vstack((x_axis, y_axis, z_axis))
    t = eye

    T_cam2world = np.zeros([4,4])
    T_cam2world[:3,:3] = R.T
    T_cam2world[:3, 3] = t
    T_cam2world[3,3] = 1.
    return T_cam2world
    


