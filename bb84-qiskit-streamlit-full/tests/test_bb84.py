import numpy as np
from src.bb84 import sift_key, compute_qber, run_bb84

def test_sift_and_qber_no_noise():
    alice_bits = np.array([0,1,1,0,1,0,1,0])
    alice_bases = ['Z','X','Z','X','Z','X','Z','X']
    bob_bases = ['Z','X','Z','X','Z','X','Z','X']
    bob_results, _ = run_bb84(alice_bits, alice_bases, bob_bases, intercept_fraction=0.0)
    a_s, b_s, pos = sift_key(alice_bits, alice_bases, bob_results, bob_bases)
    assert len(a_s) == len(b_s)
    qber = compute_qber(a_s, b_s)
    assert qber == 0.0

def test_intercept_increases_errors():
    alice_bits = np.random.randint(0,2,16)
    alice_bases = np.random.choice(['Z','X'], size=16)
    bob_bases = np.random.choice(['Z','X'], size=16)
    bob_clean, _ = run_bb84(alice_bits, alice_bases, bob_bases, intercept_fraction=0.0)
    a_s_c, b_s_c, _ = sift_key(alice_bits, alice_bases, bob_clean, bob_bases)
    qber_clean = compute_qber(a_s_c, b_s_c)
    bob_att, _ = run_bb84(alice_bits, alice_bases, bob_bases, intercept_fraction=0.5)
    a_s_a, b_s_a, _ = sift_key(alice_bits, alice_bases, bob_att, bob_bases)
    qber_att = compute_qber(a_s_a, b_s_a)
    assert qber_att >= qber_clean
