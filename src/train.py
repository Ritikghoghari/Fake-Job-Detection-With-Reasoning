import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
from scipy.sparse import hstack
from lightgbm import LGBMClassifier
from sentence_transformers import SentenceTransformer

from data_processing import prepare_features, create_train_test, vectorize_text

ART_DIR = "../model_artifacts"

# --------------------------------------------------------------------
def train_tfidf_baseline(df):
    X_train, X_test, y_train, y_test = create_train_test(df)
    Xtr_text = X_train['combined'].tolist()
    Xte_text = X_test['combined'].tolist()
    Xtr_tf, Xte_tf, tf = vectorize_text(Xtr_text, Xte_text)

    tr_tab = X_train[['company_present','has_salary','location_present']].values
    te_tab = X_test[['company_present','has_salary','location_present']].values
    Xtr = hstack([Xtr_tf, tr_tab])
    Xte = hstack([Xte_tf, te_tab])

    model = LGBMClassifier(n_estimators=300, class_weight='balanced', random_state=42)
    model.fit(Xtr, y_train)
    yprob = model.predict_proba(Xte)[:,1]
    print("\n[TF-IDF] AUC:", roc_auc_score(y_test, yprob))
    print(classification_report(y_test, (yprob>=0.5).astype(int)))

    os.makedirs(ART_DIR, exist_ok=True)
    joblib.dump({'model': model, 'tf': tf}, os.path.join(ART_DIR, "lightgbm_pipeline.joblib"))
    print("✅ Saved TF-IDF model → model_artifacts/lightgbm_pipeline.joblib")

# --------------------------------------------------------------------
def train_local_embed_classifier_and_anomaly(df):
    print("\nBuilding local embeddings (Sentence-Transformers)…")
    model_name = "all-MiniLM-L6-v2"     # small, fast, 384-dim vectors
    embedder = SentenceTransformer(model_name)

    texts = df["combined"].tolist()
    embs = embedder.encode(texts, show_progress_bar=True, batch_size=64)
    E = np.array(embs, dtype=np.float32)
    y = df["fraudulent"].astype(int).values

    # --- Logistic Regression classifier ---
    clf = LogisticRegression(max_iter=2000, class_weight="balanced")
    clf.fit(E, y)
    yprob = clf.predict_proba(E)[:,1]
    auc = roc_auc_score(y, yprob)
    print(f"[Embed-LogReg] AUC (apparent): {auc:.3f}")
    joblib.dump(clf, os.path.join(ART_DIR, "embed_classifier.joblib"))
    print("✅ Saved embedding classifier → model_artifacts/embed_classifier.joblib")

    # --- Isolation Forest for anomaly detection on REAL jobs only ---
    real_E = E[y==0]
    if len(real_E) >= 10:
        iso = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
        iso.fit(real_E)
        joblib.dump(iso, os.path.join(ART_DIR, "iso_forest.joblib"))
        print("✅ Saved Isolation Forest → model_artifacts/iso_forest.joblib")
    else:
        print("⚠️ Not enough REAL samples for Isolation Forest; skipping.")

# --------------------------------------------------------------------
def main():
    os.makedirs(ART_DIR, exist_ok=True)
    df = pd.read_csv("../data/merged_fake_job_dataset.csv")
    df = prepare_features(df)

    # Always train baseline
    train_tfidf_baseline(df)

    # Local embedding + anomaly
    train_local_embed_classifier_and_anomaly(df)

if __name__ == "__main__":
    main()
