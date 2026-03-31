import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# ---------- LOAD ----------
df = pd.read_csv("fitness_data.csv")

# ---------- CLEAN ----------
df = df.dropna()
df = df.drop_duplicates()

# ---------- FEATURE ENGINEERING ----------
df["Intensity"] = df["Heart_Rate"] / df["Duration"].replace(0, 1)

# ---------- FEATURES ----------
X = df[["Duration", "Heart_Rate", "Intensity"]]
y = df["Calories"]

# ❗ FIX: ensure enough data
if len(df) < 15:
    print("⚠️ Dataset too small → using full data for training")
    X_train, X_test, y_train, y_test = X, X, y, y
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

# ---------- MODEL ----------
model1 = LinearRegression()
model1.fit(X_train, y_train)

model2 = DecisionTreeRegressor(random_state=42)
model2.fit(X_train, y_train)

# ---------- EVALUATION ----------
pred1 = model1.predict(X_test)
pred2 = model2.predict(X_test)

try:
    print("\n📊 MODEL EVALUATION")
    print("----------------------")
    print(f"Linear Regression R2: {r2_score(y_test, pred1):.3f}")
    print(f"Decision Tree R2:    {r2_score(y_test, pred2):.3f}")
    print(f"MAE:                {mean_absolute_error(y_test, pred1):.2f}")
except:
    print("⚠️ Evaluation skipped due to small dataset")

# ---------- SAVE ----------
joblib.dump(model1, "calorie_model.pkl")

print("\n✅ MODEL TRAINED & SAVED 💀🔥")