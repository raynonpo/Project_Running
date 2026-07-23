
import pandas as pd
import torch
# from transformers import TimesFm2_5ModelForPrediction
import xgboost as xgb
from datetime import date
today = date.today()
dfList={}
Laplist=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
# model = TimesFm2_5ModelForPrediction.from_pretrained("google/timesfm-2.5-200m-transformers")
# model = model.to(torch.float32).eval()
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.05,
    objective='reg:squarederror' # Explicitly tells XGBoost to predict continuous numbers
)


def tohms(total_seconds):
    # Ensure total_seconds is treated as an integer
    total_seconds = int(total_seconds)

    hours = total_seconds // 3600  # No comma!
    minutes = (total_seconds % 3600) // 60  # No comma!
    seconds = total_seconds % 60

    # Use an f-string to format as HH:MM:SS
    # ':02d' ensures single digits get a leading zero (e.g., '05' instead of '5')
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
predictlaps=[]
for lap in Laplist:
    dfList[lap]=pd.read_csv(f"10KByLaps/10KMRun_Lap{lap}.csv")
    X_train = dfList[lap].copy()
    y_train = dfList[lap][["Avg_Pace_min_km"]]
    model.fit(X_train, y_train)
    next_features = X_train.iloc[[-1]]
    predicted_next_value = model.predict(next_features)
    predictlaps.append({"Lap":lap,"Avg_Pace_min_km":tohms(predicted_next_value)})

DF=pd.DataFrame(predictlaps)
DF.to_csv(f"Prediction/Prediction_{today}")
print(DF)
