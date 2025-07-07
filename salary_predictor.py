import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Load salary dataset
df = pd.read_csv("data/salary_dataset.csv")

X = df[["job_role", "experience", "skills_count"]]
y = df["salary"]

# Encoding for job roles
preprocessor = ColumnTransformer([
    ("encoder", OneHotEncoder(handle_unknown="ignore"), ["job_role"])
], remainder="passthrough")

# Create ML pipeline
model = Pipeline([
    ("pre", preprocessor),
    ("reg", LinearRegression())
])

# Train the model
model.fit(X, y)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/salary_model.pkl")
