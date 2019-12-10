import numpy
import pandas

from streets.curvature import curvature
from shared import constants as c


def analysis(streets, regions, kwargs):
    res = pandas.DataFrame()
    for i, r in regions.iterrows():
        res.loc[i, c.R] = r[c.R]
        res.loc[i, c.A] = r[c.G].area
        r_streets = streets[streets[kwargs[c.RV]] == r[c.R]]
        r_curvatures = _curvature_per_street(r_streets)
        for m in METRICS:
            if _should_apply(m, kwargs["method"]):
                res = METRICS[m](i, res, r_streets, r_curvatures, kwargs)
    print(res)
    if kwargs["output_dir"] != "none":
        res.to_csv(f"{kwargs['output_dir']}results.csv", index=False)


def _should_apply(case, selections):
    if "all" in selections:
        return True
    if any([case in m for m in selections]):
        return True
    return False


def _curvature_per_street(streets):
    return [curvature(numpy.array(list(s.coords))) for s in streets["geometry"]]


def _methods(case, selections):
    s = [m for m in selections if "range" in m]
    if "all" in selections:
        s.append("all")
    return s


def _aggregate(i, case, results, values, kwargs):
    for a in c.AGGREGATES:
        if _should_apply(a, _methods(case, kwargs["method"])):
            results.loc[i, f"{case}_{a}"] = getattr(numpy, a)(values)
    return results


def _range(i, results, streets, curvatures, kwargs):
    values = [c.max() - c.min() for c in curvatures]
    return _aggregate(i, "range", results, values, kwargs)


def _variance(i, results, streets, curvatures, kwargs):
    values = [c.var() for c in curvatures]
    return _aggregate(i, "variance", results, values, kwargs)


def _direction_changes(i, results, streets, curvatures, kwargs):
    values = [_count_direction_change(p) for p in curvatures]
    return _aggregate(i, "direction_changes", results, values, kwargs)


def _count_direction_change(points):
    count = 0
    if len(points) <= 2:
        return count
    current_direction = 1 if points[1] - points[0] > 0 else -1
    for i in range(1, len(points) - 1):
        new_direction = points[i + 1] - points[i]
        if new_direction * current_direction < 0:
            # Negative mult ==> direction change
            current_direction = new_direction
            count += 1
    return count


def _density_streets(i, results, streets, curvatures, kwargs):
    a = results.loc[i, c.A]
    results.loc[i, "n_streets"] = streets.shape[0]
    results.loc[i, "density_streets"] = results.loc[i, "n_streets"] / a
    return results


def _density_points(i, results, streets, curvatures, kwargs):
    a = results.loc[i, c.A]
    points = [[p[0], p[1]] for g in streets[c.G] for p in g.coords]
    results.loc[i, "n_points"] = len(points)
    results.loc[i, "density_points"] = results.loc[i, "n_points"] / a
    return results


METRICS = {
    "range": _range,
    "variance": _variance,
    "direction_changes": _direction_changes,
    "density_streets": _density_streets,
    "density_points": _density_points,
}
