import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = "models/intelligent_qkd_detector.pkl"

def generate_training_data(n_samples=400):
    """Generate synthetic QBER-based features for training."""
    np.random.seed(42)
    data = []
    labels = []

    for _ in range(n_samples):
        noise_p = np.random.uniform(0, 0.4)
        intercept_frac = np.random.uniform(0, 1)

        # Simulate approximate QBER behavior
        if intercept_frac == 0 and noise_p < 0.05:
            label = 'clean'
            qber = np.random.normal(0.02, 0.01)
        elif intercept_frac == 0 and noise_p > 0.05:
            label = np.random.choice(['bitflip', 'phaseflip', 'depolarizing'])
            base = {'bitflip': 0.08, 'phaseflip': 0.10, 'depolarizing': 0.12}[label]
            qber = np.random.normal(base + noise_p/4, 0.02)
        else:
            label = 'eavesdropping'
            qber = np.random.normal(0.15 + 0.2*intercept_frac, 0.03)

        qber_series = np.clip(np.random.normal(qber, 0.02, 32), 0, 1)
        mean_qber = np.mean(qber_series)
        std_qber = np.std(qber_series)
        data.append([mean_qber, std_qber, noise_p, intercept_frac])
        labels.append(label)

    df = pd.DataFrame(data, columns=['mean_qber', 'std_qber', 'noise_p', 'intercept_frac'])
    df['label'] = labels
    return df


def train_model(save_path=MODEL_PATH):
    """Train and save the intelligent QKD classifier."""
    df = generate_training_data()
    le = LabelEncoder()
    df['label_enc'] = le.fit_transform(df['label'])

    X = df[['mean_qber', 'std_qber', 'noise_p', 'intercept_frac']].values
    y = df['label_enc'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42)
    clf.fit(X_train, y_train)

    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Model trained with accuracy: {acc:.3f}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump((clf, le), save_path)
    print(f"Model saved to {save_path}")


def load_model():
    """Load trained model."""
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)


def predict_disturbance(mean_qber, std_qber, noise_p, intercept_frac):
    """Predict likely disturbance source based on given features."""
    clf, le = load_model()
    features = np.array([[mean_qber, std_qber, noise_p, intercept_frac]])
    probs = clf.predict_proba(features)[0]
    pred_label = le.inverse_transform([np.argmax(probs)])[0]
    confidence = np.max(probs)
    return pred_label, confidence
