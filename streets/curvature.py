import numpy


def curvature(points):
    #
    # General parametrization method for curvature:
    # - https://en.wikipedia.org/wiki/Curvature
    #
    dx_dt = numpy.gradient(points[:, 0])
    dy_dt = numpy.gradient(points[:, 1])
    d2x_dt2 = numpy.gradient(dx_dt)
    d2y_dt2 = numpy.gradient(dy_dt)
    return (
        numpy.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2)
        / (dx_dt * dx_dt + dy_dt * dy_dt) ** 1.5
    )
