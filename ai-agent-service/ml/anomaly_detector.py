import numpy as np
from sklearn.ensemble import IsolationForest


def extract_features(meta: dict) -> list:
    """
    Extract a simple numerical feature vector from CAD metadata.
    Features: [num_lines, num_circles, width, height]
    """
    counts = meta.get("entity_counts", {})
    return [
        counts.get("LINE", 0),
        counts.get("CIRCLE", 0),
        meta.get("width", 0.0),
        meta.get("height", 0.0)
    ]

def detect_anomaly(old_meta: dict, new_meta: dict) -> tuple[bool, float]:
    """
    Train a lightweight Isolation Forest on a mock historical dataset plus the old_meta.
    Then score the new_meta to see if it's an anomaly.
    Returns: (is_anomalous, risk_score)
    """
    old_features = extract_features(old_meta)
    new_features = extract_features(new_meta)
    
    # In a real system, we'd load a pre-trained model on thousands of past PRs.
    # Here, we simulate a dataset of 'normal' variations around the old_features.
    np.random.seed(42)
    base_data = np.array(old_features)
    
    # Generate 100 samples of "normal" historical commits (adding some noise)
    noise = np.random.normal(0, max(1, 0.05 * np.mean(base_data)), (100, 4))
    X_train = np.maximum(0, base_data + noise) # Ensure no negative entities
    
    # Train Isolation Forest
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(X_train)
    
    # Predict on the new metadata
    X_test = np.array([new_features])
    prediction = clf.predict(X_test)[0] # 1 for inlier, -1 for outlier
    
    # Decision function returns anomaly score. Lower (negative) means more anomalous.
    score_raw = clf.decision_function(X_test)[0]
    
    # Normalize risk score between 0 and 1 (1 being highest risk)
    # score_raw is roughly between -0.5 and 0.5. 
    # Let's map negative values to high risk.
    risk_score = float(max(0.0, min(1.0, 0.5 - score_raw)))
    
    is_anomalous = prediction == -1
    
    return bool(is_anomalous), risk_score
