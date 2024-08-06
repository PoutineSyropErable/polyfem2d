import numpy as np
import meshio

def generate_tetrahedral_grid(nx, ny, nz):
    # Generate grid points
    points = np.array([[x, y, z] for z in range(nz+1) for y in range(ny+1) for x in range(nx+1)])
    
    # Generate tetrahedral cells
    tetrahedra = []
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                # Indices of the 8 corners of the cube
                v0 = i + j*(nx+1) + k*(nx+1)*(ny+1)
                v1 = v0 + 1
                v2 = v0 + (nx+1)
                v3 = v1 + (nx+1)
                v4 = v0 + (nx+1)*(ny+1)
                v5 = v1 + (nx+1)*(ny+1)
                v6 = v2 + (nx+1)*(ny+1)
                v7 = v3 + (nx+1)*(ny+1)
                
                # Divide the cube into 5 tetrahedra
                tetrahedra.append([v0, v1, v2, v6])
                tetrahedra.append([v0, v2, v3, v6])
                tetrahedra.append([v0, v3, v7, v6])
                tetrahedra.append([v0, v7, v4, v6])
                tetrahedra.append([v0, v4, v5, v6])
    
    tetrahedra = np.array(tetrahedra)
    
    return points, tetrahedra

# Create a 5x5x5 grid
nx, ny, nz = 5, 5, 5
points, tetrahedra = generate_tetrahedral_grid(nx, ny, nz)

# Create the mesh object
mesh = meshio.Mesh(points, [("tetra", tetrahedra)])

# Write the mesh to a file (e.g., VTU format)
meshio.write("cubic_grid_tetra.vtu", mesh)

# Alternatively, you can save in other formats like .msh, .xdmf, etc.
meshio.write("cubic_grid_tetra.msh", mesh)
