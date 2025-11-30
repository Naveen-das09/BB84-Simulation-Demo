🧪 BB84 Quantum Key Distribution — Qiskit + Streamlit Demo

A complete, interactive demonstration of the BB84 Quantum Key Distribution (QKD) protocol built with:

✅ Python
✅ Qiskit (Aer simulator)
✅ Streamlit UI
✅ Custom noise models
✅ Eavesdropper simulation (Eve)
✅ ML-based QBER anomaly detector

This project simulates how Alice and Bob establish a secure quantum key, how noise & eavesdropping affect QBER, and visualizes the full protocol step-by-step.

🎯 Features
🔹 1. Full BB84 Protocol Simulation

Random bit generation

Random basis selection (X/Z)

Qubit preparation

Transmission through noise models

Measurement by Bob

Basis reconciliation

Sifting

QBER computation

🔹 2. Noise Models Implemented

Inside noise_models.py:

Depolarizing noise

Bit-flip noise

Phase-flip noise

Custom combined noise

You can toggle noise strength from the Streamlit UI.

🔹 3. Eavesdropper (Eve) Simulation

eavesdropper.py simulates different types of Eve:

Intercept–Resend

Measurement in random bases

Measurement in chosen basis

Aggressive Eve (high disturbance)

Eve automatically increases QBER — visually shown.

🔹 4. Machine Learning QBER Detector

Your ml_detector.py includes an ML model that predicts abnormal QBER spikes:

Logistic regression classifier

Detects “attack vs no attack”

Shown live in UI boxes

🔹 5. Beautiful Streamlit UI

app/streamlit_app.py includes:

Animated QBER alerts

Highlighted key differences

Step-by-step visual guide

Real-time measurement results

📂 Project Structure
.
├── app/
│   └── streamlit_app.py         # UI application
│
├── src/
│   ├── bb84.py                  # core BB84 protocol logic
│   ├── noise_models.py          # depolarization, bitflip, etc.
│   ├── eavesdropper.py          # Eve simulations
│   ├── ml_detector.py           # ML model to detect anomalies
│   └── __pycache__/
│
├── assets/                      # images, diagrams (optional)
│
├── notebooks/
│   └── demo.ipynb               # Jupyter demonstration
│
├── tests/                       # unit tests (optional)
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore

🚀 How to Run
1. Clone the repository
git clone https://github.com/<your-username>/bb84-qiskit-streamlit.git
cd bb84-qiskit-streamlit

2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.\.venv\Scripts\activate    # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the Streamlit app
streamlit run app/streamlit_app.py


You will see something like:

Local URL: http://localhost:8501
Network URL: http://172.xx.xx.xx:8501


Open it in your browser, and you're ready to explore the quantum world ⭐
