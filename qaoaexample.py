import networkx as nx
import numpy as np
from docplex.mp.model import Model

from qiskit import BasicAer
from qiskit.aqua import aqua_globals, QuantumInstance
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import SPSA
from qiskit.optimization.ising import docplex, max_cut
from qiskit.optimization.ising.common import sample_most_likely

# Generate a graph of 4 nodes
n = 4
graph = nx.Graph()
graph.add_nodes_from(np.arange(0, n, 1))
elist = [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (1, 2, 1.0), (1, 3, 1.0), (2, 3, 1.0)]
graph.add_weighted_edges_from(elist)
# Compute the weight matrix from the graph
w = np.zeros([n, n])
for i in range(n):
    for j in range(n):
        temp = graph.get_edge_data(i, j, default=0)
        if temp != 0:
            w[i, j] = temp['weight']

# Create an Ising Hamiltonian with docplex.
mdl = Model(name='max_cut')
mdl.node_vars = mdl.binary_var_list(list(range(n)), name='node')
maxcut_func = mdl.sum(w[i, j] * mdl.node_vars[i] * (1 - mdl.node_vars[j])
                      for i in range(n) for j in range(n))
mdl.maximize(maxcut_func)
qubit_op, offset = docplex.get_operator(mdl)

# Run quantum algorithm QAOA on qasm simulator
seed = 40598
aqua_globals.random_seed = seed

spsa = SPSA(max_trials=250)
qaoa = QAOA(qubit_op, spsa, p=2)
backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024, seed_simulator=seed,
                                   seed_transpiler=seed)
result = qaoa.run(quantum_instance)
parameters=qaoa.optimal_params

x = sample_most_likely(result['eigvecs'][0])
print('energy:', result['energy'])
print('time:', result['eval_time'])
print('max-cut objective:', result['energy'] + offset)
print('solution:', max_cut.get_graph_solution(x))
print('solution objective:', max_cut.max_cut_value(x, w))
print('optimal angles:', parameters)