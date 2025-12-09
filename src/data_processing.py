import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

def basic_clean(text):
    if pd.isna(text): return ""
    text = str(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'http\S+', '', text)
    return text.strip().lower()

def prepare_features(df: pd.DataFrame):
    df = df.copy()
    for c in ["title","company_profile","description","requirements","benefits","salary_range","location"]:
        if c not in df.columns:
            df[c] = ""
    df["combined"] = (
        df["title"].fillna("") + " . " +
        df["company_profile"].fillna("") + " . " +
        df["description"].fillna("") + " . " +
        df["requirements"].fillna("") + " . " +
        df["benefits"].fillna("")
    ).map(basic_clean)
    df["has_salary"] = df["salary_range"].fillna("").apply(lambda x: 0 if x=="" else 1)
    df["location_present"] = df["location"].fillna("").apply(lambda x: 0 if x=="" else 1)
    df["company_present"] = df["company_profile"].fillna("").apply(lambda x: 0 if x.strip()=="" else 1)
    return df

def vectorize_text(train_texts, test_texts, max_features=15000):
    tf = TfidfVectorizer(max_features=max_features, ngram_range=(1,2))
    X_train = tf.fit_transform(train_texts)
    X_test = tf.transform(test_texts)
    return X_train, X_test, tf

def create_train_test(df, label_col='fraudulent', test_size=0.2, random_state=42):
    df = df.copy()
    df[label_col] = df[label_col].fillna(0).astype(int)
    X = df[['combined','company_present','has_salary','location_present']]
    y = df[label_col]
    return train_test_split(X, y, stratify=y, test_size=test_size, random_state=random_state)
