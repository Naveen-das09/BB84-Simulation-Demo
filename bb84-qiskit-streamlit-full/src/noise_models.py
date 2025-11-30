from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error

def depolarizing_noise_model(p: float):
    nm = NoiseModel()
    err = depolarizing_error(p, 1)
    nm.add_all_qubit_quantum_error(err, ['id', 'u1', 'u2', 'u3', 'h', 'x'])
    return nm

def bitflip_noise_model(p: float):
    nm = NoiseModel()
    err = pauli_error([('X', p), ('I', 1 - p)])
    nm.add_all_qubit_quantum_error(err, ['id', 'u1', 'u2', 'u3', 'h', 'x'])
    return nm

def phaseflip_noise_model(p: float):
    nm = NoiseModel()
    err = pauli_error([('Z', p), ('I', 1 - p)])
    nm.add_all_qubit_quantum_error(err, ['id', 'u1', 'u2', 'u3', 'h', 'x'])
    return nm
