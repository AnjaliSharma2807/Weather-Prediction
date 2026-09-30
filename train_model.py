import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


# ---------------------------------------------------------
# CREATE SAMPLE HISTORICAL WEATHER DATA
# ---------------------------------------------------------

np.random.seed(42)

rows = 1000

df = pd.DataFrame({

    "humidity": np.random.uniform(
        30, 95, rows
    ),

    "pressure": np.random.uniform(
        990, 1030, rows
    ),

    "wind_speed": np.random.uniform(
        0, 35, rows
    ),

    "rainfall": np.random.uniform(
        0, 20, rows
    )
})


# ---------------------------------------------------------
# CREATE TARGET
# ---------------------------------------------------------

df["temperature"] = (
    38
    - (df["humidity"] * 0.08)
    + (df["pressure"] - 1000) * 0.05
    - (df["rainfall"] * 0.15)
    - (df["wind_speed"] * 0.03)
    + np.random.normal(0, 2, rows)
)


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------

X = df[
    [
        "humidity",
        "pressure",
        "wind_speed",
        "rainfall"
    ]
]

y = df["temperature"]


# ---------------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# EVALUATION
# ---------------------------------------------------------

predictions = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions
)


print(
    f"Model MAE: {mae:.2f} °C"
)


# ---------------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------------

joblib.dump(
    model,
    "weather_model.pkl"
)


print(
    "Model saved successfully!"
)