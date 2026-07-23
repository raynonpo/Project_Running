from sklearn.ensemble import RandomForestRegressor
import pandas as pd
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
df=pd.read_csv("../Compile10KMRun.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["month"] = df["Date"].dt.month
df["day"] = df["Date"].dt.day
df["Laps_lag1"] = df["Laps"].shift(1)
df["month_lag1"] = df["month"].shift(1)
df["day_lag1"] = df["day"].shift(1)

X_train=df.copy()
y_train=df[["Avg_Pace_min_km","Laps"]]
print(type(X_train),type(y_train))
model.fit(X_train, y_train)

importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": model.feature_importances_
})

importance.sort_values(
    "Importance",
    ascending=False
)
print(importance)
