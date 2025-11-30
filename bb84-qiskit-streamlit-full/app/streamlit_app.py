import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.bb84 import run_bb84, sift_key, compute_qber
from src.noise_models import depolarizing_noise_model, bitflip_noise_model, phaseflip_noise_model
from src.eavesdropper import InterceptResend


st.set_page_config(page_title='BB84 — Cyber Security Demo', layout='wide')

# Dark / cyber CSS

st.markdown("""
    <style>
    .pulse-alert {
        color: #ff4b4b;
        font-weight: bold;
        animation: pulse 1s infinite;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.8);
    }

    @keyframes pulse {
        0% { text-shadow: 0 0 5px rgba(255, 0, 0, 0.7); }
        50% { text-shadow: 0 0 25px rgba(255, 0, 0, 1); }
        100% { text-shadow: 0 0 5px rgba(255, 0, 0, 0.7); }
    }

    .qber-box {
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #ff4b4b;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
        animation: pulse-border 1.2s infinite;
        margin-top: 8px;
    }

    @keyframes pulse-border {
        0% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.9); }
        100% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.5); }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .css-18e3th9 {padding-top: 1rem;}
    .reportview-container {
        background: linear-gradient(180deg, #0b0f1a 0%, #071226 100%);
        color: #e6f1ff;
    }
    .stButton>button {
        background-color:#0f1724;
        color: #9be7ff;
        border-radius:8px;
    }
    .metric-label {
        color: #9be7ff;
    }
    .big-metric {
        font-size: 44px !important;
        color: #ff6b6b;
    }
    .qber-high {
        color: #ff6b6b;
        font-weight: 700;
    }
    .qber-low {
        color: #7ee787;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('BB84 Quantum Key Distribution — Cyber Security Demo')
st.write('A dark-themed interactive demo showing how QBER reveals eavesdropping. Use the controls to simulate attacks and noise.')

# Sidebar controls
with st.sidebar:
    st.header('Simulation Controls')
    n_qubits = st.slider('Number of qubits', 32, 1024, 256, step=32)
    mode = st.selectbox('Mode', ['Simple', 'With noise', 'With eavesdropping', 'Noise + Eavesdropping'])
    noise_type = st.selectbox('Noise type', ['Depolarizing', 'Bitflip', 'Phaseflip'])
    noise_p = st.slider('Noise probability', 0.0, 0.5, 0.02, 0.01)
    intercept_frac = st.slider('Eve intercept fraction', 0.0, 1.0, 0.2, 0.05)
    run_button = st.button('Run Simulation', key='run')

st.markdown('---')

if run_button:
    # Generate random inputs
    alice_bits = np.random.randint(0, 2, size=n_qubits)
    alice_bases = np.random.choice(['Z', 'X'], size=n_qubits)
    bob_bases = np.random.choice(['Z', 'X'], size=n_qubits)

    # Build noise model if needed
    noise_model = None
    if mode in ('With noise', 'Noise + Eavesdropping'):
        if noise_type == 'Depolarizing':
            noise_model = depolarizing_noise_model(noise_p)
        elif noise_type == 'Bitflip':
            noise_model = bitflip_noise_model(noise_p)
        else:
            noise_model = phaseflip_noise_model(noise_p)

    # Eavesdropper
    intercept_fraction = intercept_frac if mode in ('With eavesdropping', 'Noise + Eavesdropping') else 0.0

    bob_results, eve_flags = run_bb84(alice_bits, alice_bases, bob_bases, noise_model=noise_model, intercept_fraction=intercept_fraction, eve_strategy='random')

    a_sift, b_sift, positions = sift_key(alice_bits, alice_bases, bob_results, bob_bases)
    qber = compute_qber(a_sift, b_sift)

    # Display metrics with cyber visuals
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        st.markdown('<div class="metric-label">Sifted key length</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-metric">{len(a_sift)}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-label">QBER</div>', unsafe_allow_html=True)
        threshold = 0.11  # QBER threshold for compromised channel
        if qber > threshold:
            st.markdown(f"""
                <div class='qber-box'>
                    <h4 class='pulse-alert'>⚠️ {qber:.4f} — COMPROMISED</h4>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='big-metric' style='color:#2ecc71;'>✅ {qber:.4f} — SECURE</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('**Mode**')
        st.write(mode)
        st.markdown('**Noise p**: ' + str(noise_p))
        st.markdown('**Eve intercept frac**: ' + str(intercept_fraction))

    st.markdown('---')
    st.subheader('Sifted key (first 200 entries)')
    df = pd.DataFrame({
        'position': positions,
        'alice_bit': a_sift,
        'bob_bit': b_sift
    })
    st.dataframe(df.head(200))

    # QBER visualization
    st.subheader('QBER diagnostic — moving window error rate')
    window = 32
    if len(positions) >= window:
        errors = (a_sift != b_sift).astype(int)
        moving = np.convolve(errors, np.ones(window)/window, mode='valid')
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(moving)
        ax.set_ylabel('Error rate (window)')
        ax.set_xlabel('Window index')
        ax.set_ylim(0,1)
        ax.grid(True, linewidth=0.3)
        st.pyplot(fig)
    else:
        st.info('Not enough sifted bits to compute moving-window diagnostic.')

    # Show fraction of intercepted qubits if eavesdropping used
    if intercept_fraction > 0:
        intercepted_count = sum(eve_flags)
        st.warning(f'Eavesdropper intercepted approx {intercepted_count} qubits (simulated). QBER increase indicates intrusion.')
    st.markdown('---')
    st.download_button('Download sifted key CSV', data=df.to_csv(index=False).encode('utf-8'), file_name='bb84_sifted.csv', mime='text/csv')
