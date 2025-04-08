# import streamlit as st
# import matplotlib.pyplot as plt
# import networkx as nx
# import io

# from qiskit_aer.primitives import Sampler as AerSampler
# from qiskit_algorithms import QAOA
# from qiskit_algorithms.optimizers import COBYLA
# from qiskit_optimization import QuadraticProgram
# from qiskit_optimization.algorithms import MinimumEigenOptimizer
# from qiskit_optimization.converters import QuadraticProgramToQubo

# def create_maxcut_problem():
#     # Create a simple graph
#     G = nx.Graph()
#     G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])

#     # Draw the graph
#     pos = nx.spring_layout(G, seed=42)
#     fig, ax = plt.subplots()
#     nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, ax=ax)
#     st.pyplot(fig)

#     # Define the Max-Cut as a quadratic program
#     problem = QuadraticProgram()
#     for i in G.nodes:
#         problem.binary_var(name=f"x{i}")
#     for i, j in G.edges:
#         problem.minimize(linear=[], quadratic={(f"x{i}", f"x{j}"): -1})

#     return G, problem

# def render_qaoa():
#     st.subheader("📦 QAOA – Max-Cut Problem")
#     st.markdown("""
#     The **Quantum Approximate Optimization Algorithm (QAOA)** solves combinatorial problems such as Max-Cut.
    
#     It finds the best partition of graph nodes such that the number of "cut" edges between them is maximized.
#     """)

#     G, problem = create_maxcut_problem()

#     if st.button("▶️ Run QAOA"):
#         st.info("⏳ Solving Max-Cut using QAOA...")

#         sampler = AerSampler()
#         qaoa = QAOA(sampler=sampler, optimizer=COBYLA(maxiter=50))
#         optimizer = MinimumEigenOptimizer(qaoa)

#         qubo_converter = QuadraticProgramToQubo()
#         qubo = qubo_converter.convert(problem)
#         result = optimizer.solve(qubo)

#         # Highlight edges in the cut
#         cut_edges = []
#         partition = [i for i, x in enumerate(result.x) if x > 0.5]
#         for i, j in G.edges:
#             if (i in partition) != (j in partition):
#                 cut_edges.append((i, j))

#         pos = nx.spring_layout(G, seed=42)
#         fig, ax = plt.subplots()
#         nx.draw_networkx_nodes(G, pos, node_color='skyblue', ax=ax)
#         nx.draw_networkx_labels(G, pos, ax=ax)
#         nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray', ax=ax)
#         nx.draw_networkx_edges(G, pos, edgelist=cut_edges, edge_color='red', width=3, ax=ax)
#         st.pyplot(fig)

#         st.success(f"✅ Max-Cut Objective Value: {result.fval}")
#         st.code(f"Bitstring (solution): {result.x}", language='python')
