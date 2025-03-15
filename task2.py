import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from collections import Counter

def generatesurfaces(grid_size):
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    x, y = np.meshgrid(x, y)
    points_xy = np.vstack((x.flatten(), y.flatten())).T
    z_top = 2 * (x**2 + y**2).flatten()
    z_bottom = 2 * np.exp(-x**2 - y**2).flatten()
    points_top = np.hstack((points_xy, z_top.reshape(-1, 1)))
    points_bottom = np.hstack((points_xy, z_bottom.reshape(-1, 1)))
    return points_top, points_bottom

def plot_surface(points, simplices, title,directory):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(points[:, 0], points[:, 1], points[:, 2], triangles=simplices, cmap='viridis')
    ax.set_title(title)
    plt.savefig(directory)
    plt.show()

def filter_points(points_top, points_bottom):
    top_mask = points_top[:, 2] < points_bottom[:, 2]
    filtered_top = points_top[top_mask]
    bottom_mask = points_bottom[:, 2] > points_top[:, 2]
    filtered_bottom = points_bottom[bottom_mask]
    return filtered_top, filtered_bottom

def combine_surfaces(filtered_top, filtered_bottom):
    combined_points = np.vstack((filtered_top, filtered_bottom))
    n_top = len(filtered_top)
    side_triangles = []
    for i in range(n_top - 1):
        side_triangles.append([i, i + 1, n_top + i])
        side_triangles.append([i + 1, n_top + i + 1, n_top + i])
    side_triangles = np.array(side_triangles)
    return combined_points, side_triangles

def generate_volume_mesh(points):
    tri = Delaunay(points)
    return tri.simplices

def extract_surface_mesh_from_volume_mesh(tetrahedra):
    face_count = Counter()
    for tetra in tetrahedra:
        faces = [
            tuple(sorted((tetra[0], tetra[1], tetra[2]))),
            tuple(sorted((tetra[0], tetra[1], tetra[3]))),
            tuple(sorted((tetra[0], tetra[2], tetra[3]))),
            tuple(sorted((tetra[1], tetra[2], tetra[3]))),
        ]
        for face in faces:
            face_count[face] += 1
    boundary_faces = [face for face, count in face_count.items() if count == 1]
    boundary_triangles = np.array([list(face) for face in boundary_faces])
    return boundary_triangles

#a)
grid_size = 50
points_top, points_bottom = generatesurfaces(grid_size)
filtered_top, filtered_bottom = filter_points(points_top, points_bottom)
combined_points, side_triangles = combine_surfaces(filtered_top, filtered_bottom)

#b)
tri_top = Delaunay(filtered_top[:, :2])
plot_surface(filtered_top, tri_top.simplices, 'Bottom Surface (2x^2 + 2y^2)', "./plots/task2b1")
tri_bottom = Delaunay(filtered_bottom[:, :2])
plot_surface(filtered_bottom, tri_bottom.simplices, 'Top Surface (2e^(-x^2 - y^2))', "./plots/task2b2")
combined_simplices = np.vstack((tri_top.simplices, tri_bottom.simplices + len(filtered_top), side_triangles))
plot_surface(combined_points, combined_simplices, 'Combined Surface (Enclosed Volume)', "./plots/task2b3")
    
#c)
tetrahedra = generate_volume_mesh(combined_points)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(combined_points[:, 0], combined_points[:, 1], combined_points[:, 2], triangles=side_triangles, cmap='viridis')
ax.set_title('Volume Mesh (Reduced Density)')
plt.savefig("./plots/task2c")
plt.show()
    
#d)
surface_triangles = extract_surface_mesh_from_volume_mesh(tetrahedra)
plot_surface(combined_points, surface_triangles, 'Surface Mesh from Volume Mesh',"./plots/task2d")