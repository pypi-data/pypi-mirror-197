from matplotlib import pyplot as plt
from pyroll.report import hookimpl
from pyroll.core import RollPass, Unit


@hookimpl
def unit_plot(unit: Unit):
    """Plot roll pass contour and its profiles"""
    if isinstance(unit, RollPass):
        fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
        ax: plt.Axes = fig.subplots()

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)
        plt.title("Lendl Areas and Boundaries")

        ax.fill(*unit.in_profile.lendl_section.boundary.xy, color="red", alpha=0.5)
        ax.fill(*unit.out_profile.lendl_section.boundary.xy, color="blue", alpha=0.5)
        for cl in unit.contour_lines:
            ax.plot(*cl.xy, color="k")

        return fig
