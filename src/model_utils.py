import joblib
import numpy as np
from scipy.sparse import hstack
import shap

ARTIFACT = "../model_artifacts/lightgbm_pipeline.joblib"

def load_model():
    d = joblib.load(ARTIFACT)
    return d['model'], d['tf']

def predict_raw(model, tf, data_dict):
    # data_dict must contain 'combined' and tabular features
    v = tf.transform([data_dict['combined']])
    tab = np.array([[data_dict.get('company_present',0),
                     data_dict.get('has_salary',0),
                     data_dict.get('location_present',0)]])
    X = hstack([v, tab])
    proba = model.predict_proba(X)[:,1][0]
    pred = int(proba > 0.5)
    return pred, proba, X

def explain_shap(model, X):
    # compute SHAP values (TreeExplainer for LightGBM)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    return shap_values
