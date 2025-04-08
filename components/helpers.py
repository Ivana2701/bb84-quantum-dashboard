import random
import pandas as pd
from qiskit import QuantumCircuit
from qiskit_aer.primitives import SamplerV2
# from qiskit.primitives.sampler import Sampler


def sample_bit(qc: QuantumCircuit) -> int:
    sampler = SamplerV2()
    job = sampler.run([qc], shots=1)
    result = job.result()
    counts = result[0].data.c0.get_counts()
    return int(list(counts.keys())[0])

def bb84_simulation(n=20, eve_enabled=False):
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(n)]
    eve_bases = [random.choice(['+', 'x']) for _ in range(n)] if eve_enabled else [''] * n
    bob_bases = [random.choice(['+', 'x']) for _ in range(n)]
    bob_results = []
    eve_results = [] if eve_enabled else [''] * n

    for i in range(n):
        qc = QuantumCircuit(1, 1)
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 'x':
            qc.h(0)
        if eve_enabled:
            if eve_bases[i] == 'x':
                qc.h(0)
            qc.measure(0, 0)
            eve_bit = sample_bit(qc)
            eve_results.append(eve_bit)
            qc = QuantumCircuit(1, 1)
            if eve_bit == 1:
                qc.x(0)
            if eve_bases[i] == 'x':
                qc.h(0)
        if bob_bases[i] == 'x':
            qc.h(0)
        qc.measure(0, 0)
        bob_bit = sample_bit(qc)
        bob_results.append(bob_bit)

    shared_bits_alice = [alice_bits[i] for i in range(n) if alice_bases[i] == bob_bases[i]]
    shared_bits_bob = [bob_results[i] for i in range(n) if alice_bases[i] == bob_bases[i]]
    errors = sum(a != b for a, b in zip(shared_bits_alice, shared_bits_bob))
    error_rate = errors / len(shared_bits_alice) if shared_bits_alice else 0

    return {
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "eve_bases": eve_bases,
        "eve_results": eve_results,
        "shared_key_alice": shared_bits_alice,
        "shared_key_bob": shared_bits_bob,
        "error_rate": error_rate
    }

def create_bit_flow_table(result, eve_enabled):
    data = []
    for i in range(len(result["alice_bits"])):
        row = {
            "Index": i,
            "Alice Bit": result["alice_bits"][i],
            "Alice Basis": result["alice_bases"][i],
            "Bob Basis": result["bob_bases"][i],
            "Bob Bit": result["bob_results"][i],
            "Match?": "✅" if result["alice_bases"][i] == result["bob_bases"][i] and result["alice_bits"][i] == result["bob_results"][i] else "⚠️"
        }
        if eve_enabled:
            row["Eve Basis"] = result["eve_bases"][i]
            row["Eve Bit"] = result["eve_results"][i]
        data.append(row)
    return pd.DataFrame(data)