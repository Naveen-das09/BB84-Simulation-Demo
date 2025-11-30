🧪 BB84 Quantum Key Distribution — Qiskit + Streamlit Demo

This project is an interactive demonstration of the BB84 Quantum Key Distribution (QKD) protocol using:

Python

Qiskit (Aer simulator)

Streamlit UI

Custom noise models

Eavesdropper (Eve) simulation

ML-based QBER anomaly detection

It shows how Alice and Bob establish a secure quantum key, how noise & eavesdropping affect QBER, and visualizes the protocol step-by-step.

⭐ Features
✔ Full BB84 Protocol Implementation

Random bit + basis generation

Qubit preparation

Noise simulation

Bob’s measurements

Basis reconciliation

Key sifting

QBER calculation

✔ Noise Models

Implemented in noise_models.py:

Depolarizing noise

Bit-flip noise

Phase-flip noise

Custom combined noise

✔ Eavesdropper Simulation

eavesdropper.py supports:

Intercept-Resend attack

Random basis Eve

Aggressive Eve (high disturbance)

✔ Machine-Learning Attack Detection

ml_detector.py includes:

Logistic Regression model

Detects “normal noise” vs “probable attack”

Displays result in the UI

✔ Streamlit Interface

Live protocol visualization

QBER alerts

Interactive noise sliders

Eve intensity sliders

Clean, animated UI

.
├── app/
│   └── streamlit_app.py          # Streamlit UI
│
├── src/
│   ├── bb84.py                   # Core BB84 logic
│   ├── noise_models.py           # Noise functions
│   ├── eavesdropper.py           # Eve behavior
│   ├── ml_detector.py            # ML QBER classifier
│   └── __pycache__/
│
├── notebooks/
│   └── demo.ipynb                # Example notebook
│
├── assets/                       # Images / diagrams (optional)
├── tests/                        # Unit tests (optional)
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

🚀 Run Locally
1. Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
