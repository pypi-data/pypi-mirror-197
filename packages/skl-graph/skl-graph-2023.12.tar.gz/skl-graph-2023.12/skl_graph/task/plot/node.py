# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Callable, Iterable

import numpy as nmpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as polygons_3d_t
from scipy import spatial as sptl

from skl_graph.task.plot.base import axes_t
from skl_graph.type.node import array_t, branch_node_t, end_node_t, node_t
from skl_graph.type.plot import label_style_t, node_style_t, node_styles_h


# TODO: clarify the distinction between this and dict[str, tuple[int, ...]] (used in plot.graph)
positions_as_dict_h = dict[str, tuple[array_t, ...]]


def PositionsForPlotFromDetails(
    details: Iterable[tuple[str, node_t]], TransformedY: Callable[[array_t], array_t], /
) -> positions_as_dict_h:
    """"""
    TransformedPosition = lambda _psn: (_psn[1], TransformedY(_psn[0]), *_psn[2:])

    return dict((_uid, TransformedPosition(_dtl.position)) for _uid, _dtl in details)


def PlotEndNodes(
    nodes: Iterable[tuple[str, node_t]],
    TransformedY: Callable[[array_t], array_t],
    axes: axes_t,
    node_style: node_style_t,
    /,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    positions = nmpy.array(
        tuple(_dtl.position for _, _dtl in nodes if isinstance(_dtl, end_node_t))
    )
    if positions.size == 0:
        return

    plot_style = node_style.color + node_style.type

    if positions.shape[1] == 2:
        axes.plot(
            positions[:, 1],
            TransformedY(positions[:, 0]),
            plot_style,
            markersize=node_style.size,
        )
    else:
        axes.plot3D(
            positions[:, 1],
            TransformedY(positions[:, 0]),
            positions[:, 2],
            plot_style,
            markersize=node_style.size,
        )


# By default, scatter (nodes) has a lower zorder than the one of plot (edges). Hence, an explicit zorder has to be
# passed to scatter calls.


def Plot2DBranchNodes(
    nodes: Iterable[tuple[str, node_t]],
    degrees: dict[str, int],
    TransformedY: Callable[[array_t], array_t],
    axes: axes_t,
    node_styles: node_styles_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    default_style = node_styles[None]
    for uid, details in nodes:
        if isinstance(details, branch_node_t):
            node_style = node_styles.get(degrees[uid], default_style)

            coords_0 = details.sites[1]
            coords_1 = TransformedY(details.sites[0])
            if coords_0.size > 3:
                try:
                    hull = sptl.ConvexHull(nmpy.transpose((coords_0, coords_1)))
                except sptl.QhullError:
                    # TODO: check when this happens, in particular flat convex hull
                    axes.scatter(
                        coords_0,
                        coords_1,
                        marker=node_style.type,
                        s=node_style.size,
                        c=node_style.color,
                        zorder=2,
                    )
                else:
                    vertices = hull.vertices
                    axes.fill(
                        coords_0[vertices],
                        coords_1[vertices],
                        node_style.color,
                        linewidth=None,
                    )
            elif coords_0.size == 3:
                axes.fill(coords_0, coords_1, node_style.color, linewidth=None)
            elif coords_0.size == 2:
                axes.plot(
                    coords_0,
                    coords_1,
                    node_style.color + "-",
                    linewidth=node_style.size,
                )
            else:
                axes.scatter(
                    coords_0,
                    coords_1,
                    marker=node_style.type,
                    s=node_style.size,
                    c=node_style.color,
                    zorder=2,
                )


def Plot3DBranchNodes(
    nodes: Iterable[tuple[str, node_t]],
    degrees: dict[str, int],
    TransformedY: Callable[[array_t], array_t],
    axes: axes_t,
    node_styles: node_styles_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    default_style = node_styles[None]
    for uid, details in nodes:
        if isinstance(details, branch_node_t):
            node_style = node_styles.get(degrees[uid], default_style)

            coords_0 = details.sites[1]
            coords_1 = TransformedY(details.sites[0])
            coords_2 = details.sites[2]
            if coords_0.size > 3:
                # Could be > 4 with an explicit handling of ==3, but simpler this way
                try:
                    coords = nmpy.transpose((coords_0, coords_1, coords_2))
                    hull = sptl.ConvexHull(coords)
                    triangle_lst = []
                    for face in hull.simplices:
                        triangle_lst.append(
                            [coords[v_idx, :].tolist() for v_idx in face]
                        )
                    triangle_lst = polygons_3d_t(
                        triangle_lst,
                        facecolors=node_style.color,
                    )
                    axes.add_collection3d(triangle_lst)
                except:
                    axes.scatter3D(
                        coords_0,
                        coords_1,
                        coords_2,
                        marker=node_style.type,
                        s=node_style.size,
                        c=node_style.color,
                        zorder=2,
                    )
            elif coords_0.size == 3:
                triangle = list(zip(coords_0, coords_1, coords_2))
                triangle_lst = polygons_3d_t((triangle,), facecolors=node_style.color)
                axes.add_collection3d(triangle_lst)
            elif coords_0.size == 2:
                axes.plot3D(
                    coords_0,
                    coords_1,
                    coords_2,
                    node_style.color + "-",
                    linewidth=node_style.size,
                )
            else:
                axes.scatter3D(
                    coords_0,
                    coords_1,
                    coords_2,
                    marker=node_style.type,
                    s=node_style.size,
                    c=node_style.color,
                    zorder=2,
                )


def Plot3DNodeLabels(
    nodes: Iterable[str],
    positions_as_dict: positions_as_dict_h,
    axes: axes_t,
    style: label_style_t,
) -> None:
    """"""
    for node in nodes:
        axes.text(
            *positions_as_dict[node], node, fontsize=style.size, color=style.color
        )
