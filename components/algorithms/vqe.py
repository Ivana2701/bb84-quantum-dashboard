# import streamlit as st
# import matplotlib.pyplot as plt
# from qiskit_nature.second_q.drivers import PySCFDriver
# from qiskit_nature.second_q.problems import ElectronicStructureProblem
# from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
# from qiskit_nature.second_q.mappers import JordanWignerMapper
# from qiskit.primitives import Estimator
# from qiskit_algorithms import VQE
# from qiskit_algorithms.optimizers import COBYLA
# from qiskit_nature.circuit.library import UCCSD
# import io

# def render_vqe():
#     st.subheader("⚛️ VQE: Ground State Estimation for H₂")
#     st.markdown("""
#     The **Variational Quantum Eigensolver (VQE)** is a hybrid quantum algorithm used to estimate the ground-state energy of molecules.

#     We'll estimate the energy of the hydrogen molecule (H₂) at 0.735 Å bond length using a quantum circuit.
#     """)

#     if st.button("▶️ Run VQE for H₂"):
#         st.info("⏳ Running simulation...")

#         # 1. Define molecule with PySCF
#         driver = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", basis="sto3g")
#         problem = ElectronicStructureProblem(driver)

#         # 2. Transform into active space (2 electrons, 2 orbitals)
#         transformer = ActiveSpaceTransformer(num_electrons=2, num_molecular_orbitals=2)
#         problem = transformer.transform(problem)

#         # 3. Map to qubit operator
#         mapper = JordanWignerMapper()
#         second_q_op = problem.second_q_ops()[0]
#         qubit_op = mapper.map(second_q_op)

#         # 4. Setup VQE with Estimator and UCCSD ansatz
#         estimator = Estimator()
#         ansatz = UCCSD(
#             num_spatial_orbitals=problem.num_spatial_orbitals,
#             num_particles=problem.num_particles,
#             qubit_mapper=mapper
#         )
#         optimizer = COBYLA(maxiter=100)

#         vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)
#         result = vqe.compute_minimum_eigenvalue(qubit_op)

#         # 5. Show result
#         st.success("✅ VQE Completed")
#         st.markdown(f"**Ground State Energy:** `{result.eigenvalue.real:.6f} Hartree`")
#         st.code(str(result), language="python")

#         # Optional: Visual diagram
#         if st.checkbox("🔍 Show UCCSD Ansatz Circuit"):
#             fig = ansatz.decompose().draw("mpl")
#             buf = io.BytesIO()
#             fig.savefig(buf, format="png")
#             st.image(buf)
