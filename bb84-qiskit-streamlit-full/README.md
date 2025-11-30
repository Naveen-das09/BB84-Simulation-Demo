# BB84 Quantum Key Distribution — Qiskit + Streamlit (Cyber-security Theme)

Polished BB84 demo using Qiskit and a Streamlit dashboard with a cyber-security, dark-themed presentation style.
Features:

- BB84 protocol simulation (simple, noise, intercept-resend eavesdropping)
- Noise models: depolarizing, bitflip, phaseflip (Qiskit Aer noise model wrappers)
- Adjustable eavesdropper fraction and strategy (intercept-resend)
- QBER calculation and visual alerts when QBER suggests eavesdropping
- Streamlit dashboard with dark / cyber visuals for presentations
- Unit tests, docs, and example notebook

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
pip install -r requirements.txt

streamlit run app/streamlit_app.py
```

Open http://localhost:8501 to view the dashboard.
