import pandas as pd
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv("data/simulated_pue.csv", parse_dates=["timestamp"])
df["PUE"] = df["total_power"] / df["it_power"]

# Features: IT Load + Outside Temp
X = df[["it_power", "outside_temp"]]
y = df["PUE"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Example: predict PUE for IT load=160kW, temp=20°C
prediction = model.predict([[160, 20]])
print(f"Predicted PUE at 160kW IT load and 20°C: {prediction[0]:.2f}")
