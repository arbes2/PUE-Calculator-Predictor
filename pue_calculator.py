import pandas as pd

# Load data
df = pd.read_csv("data/simulated_pue.csv", parse_dates=["timestamp"])

# Calculate PUE
df["PUE"] = df["total_power"] / df["it_power"]

print("=== PUE Table ===")
print(df[["timestamp", "it_power", "total_power", "PUE"]])

# Save results
df.to_csv("data/pue_results.csv", index=False)
print("\nResults saved to data/pue_results.csv")
