import pandas as pd
import os

# Paths to your downloaded Kaggle CSVs
DATA1 = "../data/real_or_fake.csv"
DATA2 = "../data/fake_job_postings.csv"

# You may adjust these names depending on the exact filenames in your folders.
# Use os.listdir('../data') to check if needed.

# Load both datasets
df1 = pd.read_csv(DATA1, encoding='utf-8', low_memory=False)
df2 = pd.read_csv(DATA2, encoding='utf-8', low_memory=False)

print("Loaded:", df1.shape, df2.shape)

# Standardize column names (some Kaggle versions differ slightly)
df1.columns = [c.lower().strip() for c in df1.columns]
df2.columns = [c.lower().strip() for c in df2.columns]

# Ensure target column is present
if 'fraudulent' not in df1.columns:
    raise ValueError("Dataset 1 missing 'fraudulent' column")
if 'fraudulent' not in df2.columns:
    raise ValueError("Dataset 2 missing 'fraudulent' column")

# --- Keep only relevant columns ---
keep_cols = [
    "job_id",
    "title",
    "location",
    "salary_range",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "telecommuting",
    "has_company_logo",
    "has_questions",
    "employment_type",
    "required_experience",
    "required_education",
    "fraudulent"
]

df1 = df1[[c for c in keep_cols if c in df1.columns]]
df2 = df2[[c for c in keep_cols if c in df2.columns]]

# --- Combine both ---
merged = pd.concat([df1, df2], ignore_index=True)

# --- Drop duplicates (based on title+description text) ---
merged.drop_duplicates(subset=["title", "description"], inplace=True)

# --- Clean text (optional minimal) ---
for col in ["title","company_profile","description","requirements","benefits"]:
    merged[col] = merged[col].fillna("").astype(str).str.replace(r"\s+", " ", regex=True)

# --- Fill numeric / categorical ---
merged["telecommuting"] = merged["telecommuting"].fillna(0).astype(int)
merged["has_company_logo"] = merged["has_company_logo"].fillna(0).astype(int)
merged["has_questions"] = merged["has_questions"].fillna(0).astype(int)
merged["salary_range"] = merged["salary_range"].fillna("")

# --- Handle missing target safely ---
merged = merged[merged["fraudulent"].isin([0,1])]

print("Final merged shape:", merged.shape)

# --- Save cleaned dataset ---
os.makedirs("../data/cleaned", exist_ok=True)
merged.to_csv("../data/cleaned/merged_fake_job_dataset.csv", index=False, encoding='utf-8')

print("✅ Merged dataset saved to data/cleaned/merged_fake_job_dataset.csv")
