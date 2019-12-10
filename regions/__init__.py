import os
import pandas
import geopandas

from shapely.geometry import Polygon, LineString

from shared import print_

geopandas.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

COLUMNS_TO_DROP = ["Description"]


def generate_regions(**kwargs):
    print_("GENERATE REGIONS", title=True)
    print_("Parameters", section=True)
    print_(kwargs)
    data = _read_data(kwargs["inputs"])
    data = _drop_unnecessary_columns(data)
    data = _columns_to_lowercase(data)
    print_("Info", section=True)
    print_(data.crs)
    print_(data.info())
    print_("Preview", section=True)
    print_(data.head(10))
    data.to_file(kwargs["output"])


def _read_data(inputs):
    data = geopandas.GeoDataFrame()
    for _, __, files in os.walk(inputs):
        for fname in files:
            if not fname.lower().endswith(".kml"):
                continue
            data_new = geopandas.read_file(f"{inputs}{fname}", driver="KML")
            data_new["region"] = fname.replace(".kml", "").replace(".KML", "")
            if "boundary" in fname:
                # new = data_new.groupby("region").apply(_to_line)
                new = data_new.groupby("region").apply(_to_polygon)
            else:
                new = data_new.groupby("region").apply(_to_polygon)
            data = pandas.concat([data, new.reset_index()], ignore_index=True)
    data.columns = ["region", "geometry"]
    return geopandas.GeoDataFrame(data, crs={"init": "EPSG:4326"})


def _to_line(x):
    return _to_shape(LineString, x)


def _to_polygon(x):
    return _to_shape(Polygon, x)


def _to_shape(shape, x):
    return shape([p.x, p.y] for p in x["geometry"].tolist())


def _drop_unnecessary_columns(data):
    for c in COLUMNS_TO_DROP:
        if c in list(data.columns):
            data.drop(columns=c, inplace=True)
    return data


def _columns_to_lowercase(data):
    data.columns = [c.lower() for c in list(data.columns)]
    return data
