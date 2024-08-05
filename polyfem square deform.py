import numpy as np
import polyscope as ps

# Define grid dimensions
n = 10

# Create vertices for a grid of (n x n) squares
vertices = []
for i in range(n + 1):
    for j in range(n + 1):
        vertices.append([i / n, j / n, 0])

vertices = np.array(vertices, dtype=np.float32)

# Create faces (triangles) for each square
faces = []
for i in range(n):
    for j in range(n):
        # Indices of the vertices for the current square
        v0 = i * (n + 1) + j
        v1 = v0 + 1
        v2 = v0 + (n + 1)
        v3 = v2 + 1
        
        # First triangle
        faces.append([v0, v1, v2])
        # Second triangle
        faces.append([v1, v3, v2])

faces = np.array(faces, dtype=np.int32)

# Initialize Polyscope
ps.init()

# Register the mesh with Polyscope
ps_mesh = ps.register_surface_mesh("2D Grid", vertices, faces)

# Show the mesh
ps.show()
