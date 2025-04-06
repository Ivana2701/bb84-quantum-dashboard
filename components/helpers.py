import random
import pandas as pd
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def run_circuit(qc, backend):
    qc = transpile(qc, backend)
    job = backend.run(qc, shots=1, memory=True)
    result = job.result()
    return int(result.get_memory()[0])

def create_bit_flow_table(result, eve_enabled):
    data = []

    for i in range(len(result["alice_bits"])):
        alice_bit = result["alice_bits"][i]
        alice_basis = result["alice_bases"][i]
        bob_basis = result["bob_bases"][i]
        bob_bit = result["bob_results"][i]

        if alice_basis == bob_basis:
            correct = "✅" if alice_bit == bob_bit else "❌"
        else:
            correct = "⚠️"  # basis mismatch

        row = {
            "Index": i,
            "Alice Bit": alice_bit,
            "Alice Basis": alice_basis,
            "Bob Basis": bob_basis,
            "Bob Bit": bob_bit,
            "Match?": correct
        }

        if eve_enabled:
            eve_basis = result["eve_bases"][i]
            row["Eve Basis"] = eve_basis

        data.append(row)

    return pd.DataFrame(data)

def bb84_simulation(n=20, eve_enabled=False):
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(n)]
    eve_bases = [random.choice(['+', 'x']) for _ in range(n)]
    bob_bases = [random.choice(['+', 'x']) for _ in range(n)]

    simulator = Aer.get_backend('aer_simulator')
    bob_results = []

    for i in range(n):
        qc = QuantumCircuit(1, 1)

        # Alice prepares qubit
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 'x':
            qc.h(0)

        # Eve intercepts
        if eve_enabled:
            if eve_bases[i] == 'x':
                qc.h(0)
            qc.measure(0, 0)
            eve_bit = run_circuit(qc, simulator)
            qc = QuantumCircuit(1, 1)
            if eve_bit == 1:
                qc.x(0)
            if eve_bases[i] == 'x':
                qc.h(0)

        # Bob measures
        if bob_bases[i] == 'x':
            qc.h(0)
        qc.measure(0, 0)
        bob_bit = run_circuit(qc, simulator)
        bob_results.append(bob_bit)

    # Key sifting (keep only matching bases)
    shared_bits_alice = []
    shared_bits_bob = []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            shared_bits_alice.append(alice_bits[i])
            shared_bits_bob.append(bob_results[i])

    # Error rate calculation
    errors = sum([a != b for a, b in zip(shared_bits_alice, shared_bits_bob)])
    error_rate = errors / len(shared_bits_alice) if shared_bits_alice else 0

    return {
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "eve_bases": eve_bases if eve_enabled else [''] * n,
        "shared_key_alice": shared_bits_alice,
        "shared_key_bob": shared_bits_bob,
        "error_rate": error_rate
    }
