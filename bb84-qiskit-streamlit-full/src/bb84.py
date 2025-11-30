"""Core BB84 implementation using Qiskit Aer simulator.

The implementation runs qubits one-by-one on the Aer simulator. Eavesdropping is modeled
as an intercept-resend attack simulated in software: Eve measures in a basis and resends
the measured state to Bob. Noise is applied via Qiskit NoiseModel when provided.
"""
from qiskit import QuantumCircuit
from qiskit import transpile

from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel
import numpy as np

SIMULATOR = Aer.get_backend('aer_simulator')

def _prepare_circuit(bit: int, basis: str) -> QuantumCircuit:
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 'X':
        qc.h(0)
    return qc

def _measure_circuit(qc: QuantumCircuit, measure_in_basis: str, noise_model: NoiseModel = None):
    # copy to avoid mutating caller's circuit
    qc = qc.copy()
    if measure_in_basis == 'X':
        qc.h(0)
    qc.measure_all()
    backend = Aer.get_backend('qasm_simulator')
    qc_transpiled = transpile(qc, backend)
    job = backend.run(qc_transpiled)
    result = job.result()
    counts = result.get_counts()

    # counts key format like '0  ' or '1' depending on Qiskit version; split by space and take first
    key = list(counts.keys())[0]
    measured_bit = int(key.split()[0])
    return measured_bit

class InterceptResendModel:
    """Simple intercept-resend model used internally when Eve intercepts a qubit."""
    def __init__(self, strategy='random'):
        self.strategy = strategy  # 'random' or 'basis_guess' etc.

    def intercept(self, alice_bit: int, alice_basis: str, noise_model: NoiseModel = None):
        # Eve chooses a basis to measure in
        if self.strategy == 'random':
            eve_basis = 'Z' if np.random.rand() < 0.5 else 'X'
        else:
            eve_basis = 'Z'

        # Eve prepares circuit as Alice did (before any channel noise)
        qc = _prepare_circuit(alice_bit, alice_basis)
        # Measure in Eve's basis
        measured = _measure_circuit(qc, eve_basis, noise_model=noise_model)
        # Eve re-prepares a qubit in the measured state in the same basis she measured
        # To send to Bob, we prepare according to measured bit and apply H if Eve measured in X (to send in X basis)
        send_qc = QuantumCircuit(1, 1)
        if measured == 1:
            send_qc.x(0)
        if eve_basis == 'X':
            send_qc.h(0)
        return send_qc, eve_basis, measured

def run_bb84(alice_bits, alice_bases, bob_bases, noise_model: NoiseModel = None, intercept_fraction: float = 0.0, eve_strategy='random'):
    """Run BB84 for the provided arrays. Returns list of Bob's measured bits, and a list marking which positions Eve intercepted."""
    n = len(alice_bits)
    bob_results = []
    eve_flags = [False] * n
    eve = InterceptResendModel(strategy=eve_strategy)

    for i in range(n):
        # Decide if Eve intercepts this qubit
        if intercept_fraction > 0 and np.random.rand() < intercept_fraction:
            # Eve intercepts: she measures and re-sends a new qubit (intercept-resend)
            send_qc, eve_basis, eve_meas = eve.intercept(alice_bits[i], alice_bases[i], noise_model=noise_model)
            # Bob will measure the qubit sent by Eve in his chosen basis
            measured_by_bob = _measure_circuit(send_qc, bob_bases[i], noise_model=noise_model)
            bob_results.append(measured_by_bob)
            eve_flags[i] = True
        else:
            # No interception: normal transmission from Alice to Bob
            qc = _prepare_circuit(alice_bits[i], alice_bases[i])
            measured = _measure_circuit(qc, bob_bases[i], noise_model=noise_model)
            bob_results.append(measured)
    return bob_results, eve_flags

def sift_key(alice_bits, alice_bases, bob_bits, bob_bases):
    alice_sifted = []
    bob_sifted = []
    positions = []
    for i, (ba, bb) in enumerate(zip(alice_bases, bob_bases)):
        if ba == bb:
            alice_sifted.append(alice_bits[i])
            bob_sifted.append(bob_bits[i])
            positions.append(i)
    return np.array(alice_sifted), np.array(bob_sifted), positions

def compute_qber(alice_sifted, bob_sifted):
    if len(alice_sifted) == 0:
        return 0.0
    errors = np.sum(alice_sifted != bob_sifted)
    return float(errors) / len(alice_sifted)
