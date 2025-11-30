# Architecture Notes

- `src/bb84.py` core protocol using Qiskit aer_simulator
- `src/noise_models.py` supports depolarizing/bitflip/phaseflip models from Qiskit
- `src/eavesdropper.py` implements an intercept-resend attacker with adjustable fraction
- `app/streamlit_app.py` Streamlit UI (cyber-security dark theme) with controls and visual alerts
