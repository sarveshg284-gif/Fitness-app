import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Skill list (MUST MATCH app.py)
# -----------------------------
SKILL_LIST = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "power bi",
    "tableau",
    "excel",
    "aws",
    "nlp",
    "tensorflow",
    "pytorch",
    "statistics",
    "spark"
]

# -----------------------------
# Sample dataset (you can expand it)
# -----------------------------
data = [
    (["python", "sql", "data analysis", "excel"], "Data Analyst"),
    (["python", "machine learning", "statistics", "tensorflow"], "Data Scientist"),
    (["python", "aws", "spark", "sql"], "Data Engineer"),
    (["nlp", "deep learning", "python", "pytorch"], "AI Engineer"),
    (["sql", "power bi", "excel", "tableau"], "Business Analyst"),
    (["python", "machine learning", "nlp"], "Data Scientist"),
    (["aws", "spark", "python"], "Data Engineer"),
    (["deep learning", "tensorflow", "python"], "AI Engineer"),
    (["power bi", "sql", "excel"], "Business Analyst"),
    (["python", "data analysis", "statistics"], "Data Analyst")
]

# -----------------------------
# Convert to ML format
# -----------------------------
X = []
y = []

for skills, role in data:
    vector = [1 if skill in skills else 0 for skill in SKILL_LIST]
    X.append(vector)
    y.append(role)

X = np.array(X)
y = np.array(y)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Model training
# -----------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, "models/role_prediction.pkl")

print("\nModel saved successfully to models/role_prediction.pkl")
