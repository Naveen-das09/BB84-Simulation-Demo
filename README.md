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
│   └── streamlit_app.py          # Streamlit UI application
│
├── src/
│   ├── bb84.py                   # Core BB84 protocol logic
│   ├── noise_models.py           # Quantum noise models
│   ├── eavesdropper.py           # Eve attack simulation
│   ├── ml_detector.py            # Machine learning model for QBER anomaly detection
│   └── __pycache__/
│
├── notebooks/
│   └── demo.ipynb                # Notebook demonstration
│
├── assets/                       # Images, diagrams (optional)
│
├── tests/                        # Unit tests (optional)
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore


🚀 Run Locally
1️⃣ Clone the repository

git clone https://github.com/<Naveen-das09>/<BB84-Simulation-Demo>.git
cd <BB84-Simulation-Demo>

2️⃣ Create a Virtual Environment

python -m venv .venv

source .venv/bin/activate        # Mac/Linux

.\.venv\Scripts\activate         # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run Streamlit App

streamlit run app/streamlit_app.py

🔍 BB84 Protocol — Quick Explanation

Alice generates random bits.

Alice chooses random bases (X/Z) for each bit.

Alice prepares qubits in chosen bases and sends them to Bob.

Bob measures qubits in his own random bases.

Alice & Bob publicly compare bases (not bit values).

Matching basis bits form the sifted key.

🛠 Future Improvements

Real IBM Quantum hardware backend

LDPC error correction

Privacy amplification

Docker deployment

API endpoints for programmatic BB84 use
