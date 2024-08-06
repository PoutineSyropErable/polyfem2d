import meshio
import numpy as np

# Define 2D vertices and faces (triangles in this example)
points = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [0.5, 1.0],
    [1.5, 1.0]
])

# Define faces as a list of triangles (using 0-based indexing)
cells = [
    ("triangle", np.array([
        [0, 1, 2],
        [1, 3, 2]
    ]))
]

# Create a meshio Mesh object
mesh = meshio.Mesh(points, cells)

# Write the mesh to a .poly file (or any other supported format)
meshio.write("output.poly", mesh)

# Alternatively, you can use other formats like .vtk, .xml (for XDMF)
meshio.write("output.vtk", mesh)
