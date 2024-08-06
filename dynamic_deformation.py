import polyfempy as pf
import numpy as np
import meshio
import polyscope as ps

# Initialize Polyscope
ps.init()

# Initialize Polyfem settings with dynamic parameters
settings = pf.Settings(
    pde=pf.PDEs.NeoHookean,  # Using Linear Elasticity for deformation
    discr_order=1,
    tend=100.0,            # Total simulation time
    time_steps=50,       # Number of time steps
)



# Set material parameters
settings.set_material_params("type", "NeoHookean")
settings.set_material_params("E", 210000)  # Young's modulus
settings.set_material_params("nu", 0.3)    # Poisson's ratio

# Define the problem
problem = pf.Problem()

# Apply -> force on left side center
for face_id in range(6,12+1):
    problem.set_force(face_id, [1000, 0, 0])   # Force on face 8


# Apply <- force on right side center
for face_id in range(185,193+1):
    problem.set_force(face_id, [-1000, 0, 0])   # Force on face 8

# Fix the bottom faces (zero displacement)
bottom_faces = [0, 1, 20, 21, 40, 41, 60, 61, 80, 81, 100, 101, 120, 121, 140, 141, 160, 161, 180, 181]
for face in bottom_faces:
    problem.add_dirichlet_value(face, [0, 0, 0])  # Fix all displacement components

# Fix the top faces (zero displacement)
top_faces = [18, 19, 38, 39, 58, 59, 78, 79, 98, 99, 118, 119, 138, 139, 158, 159, 178, 179, 198, 199]
for face in top_faces:
    problem.add_dirichlet_value(face, [0, 0, 0])  # Fix all displacement components

# Configure settings with the problem
settings.problem = problem

# Create and configure the solver
solver = pf.Solver()
solver.set_log_level(5)
solver.settings(settings)

# Load the mesh
solver.load_mesh_from_path("grid_mesh.obj", normalize_mesh=False)

# Solve the problem
solver.solve()

# Get the solution
pts, tets, disp = solver.get_sampled_solution()

# Deformed vertices
deformed_vertices = pts + disp

print(f"disp: \n{disp}\n")
print("displacement:", np.min(disp), np.max(disp))


# Ensure vertices have 3 dimensions
if deformed_vertices.shape[1] == 2:
    deformed_vertices = np.hstack([deformed_vertices, np.zeros((deformed_vertices.shape[0], 1))])

# Save the deformed mesh using meshio
mesh = meshio.Mesh(
    points=deformed_vertices,  # Vertices of the mesh
    cells={"triangle": tets}  # Cell types and their corresponding vertex indices
)

print(f"deformed_mesh: \n {mesh}\n")

meshio.write("deformed_mesh.obj", mesh)

# Register the deformed mesh with Polyscope
ps_mesh = ps.register_surface_mesh("Deformed Grid Mesh", deformed_vertices, tets)

# Show the mesh in Polyscope
ps.show()
