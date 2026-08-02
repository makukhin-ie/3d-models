"""Render isometric PNG previews for every STL in the repo."""
import glob, os
import numpy as np
from stl import mesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

os.makedirs("previews", exist_ok=True)

for path in sorted(glob.glob("*/*.stl")):
    name = os.path.splitext(os.path.basename(path))[0]
    m = mesh.Mesh.from_file(path)
    fig = plt.figure(figsize=(5, 5), dpi=110)
    ax = fig.add_subplot(projection="3d")
    coll = mplot3d.art3d.Poly3DCollection(m.vectors, alpha=1.0)
    coll.set_facecolor("#8ab4d8")
    coll.set_edgecolor("#2f5d82")
    coll.set_linewidth(0.15)
    ax.add_collection3d(coll)
    pts = m.vectors.reshape(-1, 3)
    mins, maxs = pts.min(axis=0), pts.max(axis=0)
    center = (mins + maxs) / 2
    r = (maxs - mins).max() / 2 * 1.1
    ax.set_xlim(center[0]-r, center[0]+r)
    ax.set_ylim(center[1]-r, center[1]+r)
    ax.set_zlim(center[2]-r, center[2]+r)
    ax.set_axis_off()
    ax.view_init(elev=28, azim=-55)
    fig.tight_layout(pad=0)
    fig.savefig(f"previews/{name}.png", bbox_inches="tight", pad_inches=0.05, transparent=False)
    plt.close(fig)
    dims = maxs - mins
    print(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm, {len(m.vectors)} tris")
