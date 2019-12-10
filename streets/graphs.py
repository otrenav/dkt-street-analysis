import matplotlib.pyplot as plt

from shared import constants as c


def create_graphs(streets_orig, streets, regions, kwargs):
    fig, ax = plt.subplots(figsize=(40, 20))
    streets_orig.plot(ax=ax, edgecolor="gray", zorder=0)
    if regions is not None:
        for i, r in enumerate(sorted(regions[kwargs[c.RV]])):
            # Region perimeter
            regions[regions[kwargs[c.RV]] == r].plot(
                ax=ax,
                zorder=2,
                linewidth=5,
                facecolor=(0, 0, 0, 0),
                edgecolor=c.COLORS[i % len(c.COLORS.keys())],
            )
            # Region area
            regions[regions[kwargs[c.RV]] == r].plot(
                ax=ax,
                zorder=1,
                alpha=0.2,
                edgecolor=(0, 0, 0, 0),
                facecolor=c.COLORS[i % len(c.COLORS.keys())],
            )
    for i, region in enumerate(sorted(streets[kwargs[c.RV]].unique())):
        streets[streets[kwargs[c.RV]] == region].plot(
            ax=ax,
            zorder=3,
            linewidth=1,
            edgecolor=c.COLORS[i % len(c.COLORS.keys())],
        )

    # plt.show()
    if kwargs["output_dir"] != "none":
        plt.savefig(f"{kwargs['output_dir']}regions.png", bbox_inches="tight")

    print("\nDONE\n")
