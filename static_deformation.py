import polyfempy as pf
import numpy as np
import meshio
import polyscope as ps

# Initialize Polyscope
ps.init()

# Initialize Polyfem settings
settings = pf.Settings(
    pde=pf.PDEs.LinearElasticity, # Using Linear Elasticity for deformation
    discr_order=1
)

# Set material parameters
settings.set_material_params("E", 210000)  # Young's modulus
settings.set_material_params("nu", 0.3)    # Poisson's ratio

# Define the problem
problem = pf.Problem()

# Apply forces on specific faces
# Note: Update face indices based on your mesh
#problem.set_force(8, [0, 0, 1])  # Force on face 8
#problem.set_force(108, [0, 0, -1]) # Opposite force on face 108

# Configure settings with the problem
settings.problem = problem

# Create and configure the solver
solver = pf.Solver()
solver.settings(settings)

# Load the mesh
solver.load_mesh_from_path("grid_mesh.obj", normalize_mesh=False)

# Solve the problem




solver.solve()

# Get the solution
pts, tets, disp = solver.get_sampled_solution()

# Deformed vertices
deformed_vertices = pts + disp

print("\n\nafter getting the deformed vertises\n\n")
# Save the deformed mesh
meshio.write("deformed_mesh.obj", meshio.Mesh(vertices=deformed_vertices, cells={"triangle": tets}))

# Register the deformed mesh with Polyscope
ps_mesh = ps.register_surface_mesh("Deformed Grid Mesh", deformed_vertices, tets)

# Show the mesh
ps.show()
