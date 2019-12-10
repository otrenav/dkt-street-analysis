import geopandas
import shapely.speedups

from streets.graphs import create_graphs
from streets.analysis import analysis
from shapely.geometry import Point
from tqdm import tqdm

from shared import print_, reset_dir
from shared import constants as c

shapely.speedups.enable()


def street_metrics(**kwargs):
    print_("STREET METRICS", title=True)
    reset_dir(kwargs["output_dir"])
    print_("Parameters", section=True)
    print_(kwargs)
    print_("Data", section=True)
    regions = _read_regions_data(kwargs)
    original = _read_street_data(kwargs)
    streets, regions = _intersect_with_regions(original.copy(), regions, kwargs)
    print_("Analysis", section=True)
    analysis(streets, regions, kwargs)
    print_("Graph", section=True)
    create_graphs(original, streets, regions, kwargs)


def _read_regions_data(kwargs):
    if kwargs[c.RN] == "none":
        return None
    regions = geopandas.read_file(kwargs[c.RN])
    if "none" not in kwargs[c.RS]:
        regions = regions[regions[kwargs[c.RV]].isin(list(kwargs[c.RS]))]
    return regions.to_crs(c.PROJECTION)


def _read_street_data(kwargs):
    streets = geopandas.read_file(kwargs["input"]).to_crs(c.PROJECTION)
    if kwargs["random_sample_size"] > 0:
        streets = streets.sample(n=kwargs["random_sample_size"])
    return streets


def _intersect_with_regions(streets, regions, kwargs):
    if regions is None:
        streets[c.R] = "[single_region]"
        return streets
    indexes_to_delete = []
    streets[c.R] = None
    for i, l in tqdm(streets.iterrows(), total=streets.shape[0]):
        delete_line = True
        for p in list(l[c.G].coords):
            point = Point([p[0], p[1]])
            region = _container_region(point, regions)
            if region is not None:
                streets.loc[i, c.R] = region
                delete_line = False
                continue
        if delete_line:
            indexes_to_delete.append(i)
    streets.drop(index=indexes_to_delete, inplace=True)
    return streets, regions


def _container_region(point, regions):
    for _, region in regions.iterrows():
        if point.within(region[c.G]):
            return region[c.R]
    return None
