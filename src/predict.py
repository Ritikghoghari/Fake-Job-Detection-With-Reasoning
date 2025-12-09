import joblib
import numpy as np
from scipy.sparse import hstack
import pandas as pd
from data_processing import prepare_features
from explain_with_openai import gemini_explain

# Load model
MODEL_PATH = "../model_artifacts/lightgbm_pipeline.joblib"
artifacts = joblib.load(MODEL_PATH)
model = artifacts['model']
tf = artifacts['tf']

def predict_job_posting(title, description, company_profile="", location="", salary_range=""):
    df = pd.DataFrame([{
        "title": title,
        "description": description,
        "company_profile": company_profile,
        "requirements": "",
        "benefits": "",
        "salary_range": salary_range,
        "location": location,
        "fraudulent": 0
    }])
    df = prepare_features(df)

    text_vec = tf.transform(df["combined"])
    tab_feats = df[["company_present","has_salary","location_present"]].values
    X = hstack([text_vec, tab_feats])

    prob = model.predict_proba(X)[:,1][0]
    label = "FAKE" if prob >= 0.5 else "REAL"

    print(f"Prediction: {label} (probability: {prob:.2f})")

    # Optional Gemini reasoning
    gemini_output = gemini_explain(df["combined"].iloc[0], prob, label)
    print("\n--- Explanation ---")
    print(gemini_output.get("explanation") or gemini_output.get("error"))

if __name__ == "__main__":
    # Example test
    predict_job_posting(
        title="Work From Home Data Entry - Earn $5000/week",
        description="We offer great pay! Just send us your bank details and start today.",
        company_profile="",
        location="Remote",
        salary_range=""
    )
