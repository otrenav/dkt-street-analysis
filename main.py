import click

from regions import generate_regions as _generate_regions
from streets import street_metrics as _street_metrics
from images import image_profiles as _image_profiles


@click.group()
def main():
    pass


@main.command()
@click.option(
    "-i",
    "--input",
    default="./inputs/streets/allroads_jgd2000.shp",
    show_default=True,
    help="Shapefile with street lines used to calculate curvatures.",
)
@click.option(
    "-m",
    "--method",
    default=["all"],
    multiple=True,
    show_default=True,
    type=click.Choice(
        [
            "all",
            "range_min",
            "range_mean",
            "range_median",
            "range_max",
            "range_var",
            "variance_min",
            "variance_mean",
            "variance_median",
            "variance_max",
            "variance_var",
            "direction_changes_min",
            "direction_changes_mean",
            "direction_changes_median",
            "direction_changes_max",
            "direction_changes_var",
            "density_streets",
            "density_points",
        ],
        case_sensitive=False,
    ),
    help=(
        # TODO: Add aggregation methods
        "Methods used to calculate street statitistics. `all` indicates all "
        + "methods will be used. `range` uses the difference between the "
        + "maximum and minimum street's curvature values. `variance` "
        + "calculates the variance of the street's curvature values. "
        + "`direction_changes` makes use of the order in the street's "
        + "curvature values to calculate how many times a non-monotone change "
        + "takes place. `density_streets` divides the number of streets in a "
        + "region by the region's area in meters. `density_points` splits "
        + "streets lines into individual points and calculates density as "
        + "'points-per-squared-meter'."
    ),
)
@click.option(
    "-g",
    "--regions",
    default="./inputs/regions/shapefiles/regions.shp",
    show_default=True,
    help=(
        "Shapefile with region polygons used to filter inputs. Use `none` to "
        + "avoid filtering."
    ),
)
@click.option(
    "-r",
    "--region-variable",
    default="region",
    show_default=True,
    help=(
        "Region variable name used to filter input regions. Only used if a "
        + "--region-selection is also provided (otherwise ignored)."
    ),
)
@click.option(
    "-s",
    "--region-selection",
    multiple=True,
    default=["none"],
    show_default=True,
    help=(
        "Either `none` to intersect with all regions in the --regions file, or "
        + "for multiple region selection use `-s <region_1> -s <region_2> ...`. "
        + "Filters on --region-variable. Only used if --regions is provided "
        + "(otherwise ignored)."
    ),
)
@click.option(
    "-o",
    "--output-dir",
    default="./outputs/curvatures/",
    show_default=True,
    help=(
        "Directory to store outputs. `none` avoids storing any outputs. If "
        + "previous outputs exist matching this --output-dir they will be "
        + "deleted beforehand."
    ),
)
@click.option(
    "-n",
    "--random-sample-size",
    default=-1,
    show_default=True,
    help=(
        "If positive, use as random street sample size (used to speed up "
        + "results when developing but for actual analysis full data is "
        + "probably desired). If negative, this value is ignore (i.e. no "
        + "sampling)."
    ),
)
def street_metrics(**kwargs):
    _street_metrics(**kwargs)


@main.command()
@click.option(
    "-i",
    "--input",
    default="./inputs/regions/shapefiles/regions.shp",
    show_default=True,
    help=(
        "Shapefile with region polygons from which a random sample will be "
        + "drawn, or CSV with lng/lat coordinates for a pre-computed random "
        + "sample to override. Used only if --image-dir is not provided."
    ),
)
@click.option(
    "-d",
    "--image-dir",
    default=None,
    show_default=True,
    help=(
        "Directory with previously downloaded images (used to avoid the cost "
        + "of re-downloading images). If provided, the input file is ignored "
        + "and calculations are only applied to the images in this directory."
    ),
)
@click.option(
    "-n",
    "--random-sample-size",
    default=10,
    show_default=True,
    help=(
        "Number of points in random sample to retrieve images for. Only used "
        + "if input file is a shapefile (if CSV no sampling takes place). "
        + "Only used if random sampling is to take place (ignored otherwise)."
    ),
)
@click.option(
    "-r",
    "--region-variable",
    default="region",
    show_default=True,
    help=(
        "Region variable name used to filter input regions. Only used if a "
        + "--region-selection is also provided and random sampling takes "
        + "(otherwise ignored)."
    ),
)
@click.option(
    "-g",
    "--region-selection",
    multiple=True,
    default=["none"],
    show_default=True,
    help=(
        "Either `none` for all regions, or for multiple region selection use"
        + "`-s <region_1> -s <region_2> ...`. Filters on --region-variable. "
        + "Only used if random sampling takes place (otherwise ignored)."
    ),
)
@click.option(
    "-m",
    "--min-distance",
    default=100,
    show_default=True,
    help=(
        "Minimum meters between points in random sample. Only used if random "
        + "sampling takes place (otherwise ignored)."
    ),
)
@click.option(
    "-v",
    "--view",
    default="side",
    show_default=True,
    type=click.Choice(["side", "top"], case_sensitive=False),
    help=(
        "Either `side` or `top` (i.e. street-level vs roofs). Only used if "
        + "images are actually retrieved from Google Maps (ignored otherwise)."
    ),
)
@click.option(
    "-o",
    "--output-dir",
    default="./outputs/image_analysis/",
    show_default=True,
    help="Directory to store outputs. `none` avoids storing any outputs.",
)
@click.option(
    "--override/--no-override",
    default=False,
    show_default=True,
    help=(
        "If previous outputs are detected execution will halt unless the "
        + "`--override` options is provided. This is done to avoid "
        + "re-downloading previously retrieved images (to avoid unnecessary "
        + "costs)."
    ),
)
def image_profiles(**kwargs):
    _image_profiles(**kwargs)


@main.command()
@click.option(
    "-i",
    "--inputs",
    default="./inputs/regions/google_maps/",
    show_default=True,
    help=(
        "Directory with KML files downloaded from Google Maps with the points "
        + "that will be converted to polygon regions. Each layer in the Google "
        + "Maps map should be downloaded separately, and the corresponding "
        + "file name for each of these KML files will be taken as the region "
        + "name for each polygon."
    ),
)
@click.option(
    "-o",
    "--output",
    default="./inputs/regions/shapefiles/regions.shp",
    show_default=True,
    help=(
        "File to save polygon regions shapefile to. Various metadata files are "
        + "created around the Shapefile (e.g. regions.dbf, regions.prj, etc). "
        + "If previous files exist they will be deleted beforehand."
    ),
)
def generate_regions(**kwargs):
    _generate_regions(**kwargs)


if __name__ == "__main__":
    main()
