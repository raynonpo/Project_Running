import pandas as pd
import os
from pandas.core.interchange.dataframe_protocol import DataFrame
from ydata_profiling import ProfileReport
def rename():
    FileList = os.listdir("Data/Detail_ge10KM")
    folder = "Data/Detail_ge10KM"
    for file in FileList:
        old_path = os.path.join(folder, file)
        name, ext = os.path.splitext(file)
        new_name = f"{name}_10KM{ext}"
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)


def sec_to_hms(seconds):
    seconds = int(round(seconds))

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02d}:{m:02d}:{s:02d}"
def to_seconds(x):
    try:
        parts = str(x).split(":")

        if len(parts) == 2:  # MM:SS
            m, s = parts
            return int(m) * 60 + float(s)

        elif len(parts) == 3:  # HH:MM:SS or HH:MM:SS.ss
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)

        else:
            return None
    except:
        return None
def read_file():
    FileList=os.listdir("Data/Detail_ge10KM")
    dataframelist=[]
    for file in FileList:
        df = pd.read_csv(f"Data/Detail_ge10KM/" + file)
        Date,Location,Category=file.split(".")[0].split("_")
        df.columns = [new_ColumnName.replace(" ", "_").replace("/", "_") for new_ColumnName in df.columns]
        NewOrder=['Date','Location',"Condition_Category",'Laps', 'Time','Cumulative_Time', 'Distance_km',
        'Avg_Pace_min_km','Avg_HR_bpm', 'Max_HR_bpm', 'Total_Ascent_m', 'Total_Descent_m',
        'Avg_Run_Cadence_spm', 'Avg_Stride_Length_m', 'Calories_C','Best_Pace_min_km', 'Max_Run_Cadence_spm',
        'Moving_Time','Avg_Moving_Pace_min_km']


        df["Date"]=Date
        df["Category"] = Category
        df["Location"] = Location
        df['Condition_Category'] = df['Location'].apply(lambda x:0 if x in ["TamanWahyu", "Metropolitan"] else 1)
        print(df['Condition_Category'])
        df = df[NewOrder]
        df = df[df['Laps'] != 'Summary']
        df = df.replace("--", "", regex=False)
        for column in df:
            df[column] = df[column].astype(str)
        df["Date"] = pd.to_datetime(df["Date"], format="%d%b%Y")
        intDAta = ["Laps", "Distance_km", "Avg_HR_bpm", "Max_HR_bpm", "Total_Ascent_m", "Total_Descent_m",
                   "Avg_Run_Cadence_spm", "Avg_Stride_Length_m", "Calories_C", "Max_Run_Cadence_spm"]
        for column in intDAta:
            df[column] = df[column].replace("", 0, regex=False)
            df[column] = df[column].astype(float)
        timeds = ["Time", "Cumulative_Time", "Avg_Pace_min_km", "Best_Pace_min_km", "Moving_Time",
                  "Avg_Moving_Pace_min_km"]
        df = df[df["Distance_km"] == 1.0]
        for column in timeds:
            df[column] = df[column].apply(to_seconds)
            df[column] = df[column].astype(int)
        print(df['Condition_Category'])
            # File[column] = File[column].apply(sec_to_hms)
        Recolumn = ['Date', 'Laps', 'Time',"Condition_Category", 'Cumulative_Time',
                    'Avg_Pace_min_km', 'Avg_HR_bpm', 'Max_HR_bpm', 'Total_Ascent_m', 'Total_Descent_m',
                    'Avg_Run_Cadence_spm', 'Avg_Stride_Length_m', 'Calories_C', 'Best_Pace_min_km',
                    'Max_Run_Cadence_spm',
                    'Moving_Time', 'Avg_Moving_Pace_min_km']
        df = df[Recolumn]
        df.to_csv(f"Data/10KByDate/{Date}_{Location}_{Category}.csv",index=False)
        for column in [col for col in df.columns if col not in ["Date","Location","Category","Laps","Condition_Category"]]:

            df[column+  "_lag1"]= df[column].shift(1)
            df[column + "_lag2"] = df[column].shift(2)
            df[column + "_lag3"] = df[column].shift(3)
            df = df.fillna(0)

        dataframelist.append(df)
    result = pd.concat(dataframelist, ignore_index=True)
    result.to_csv("Predictor10KMRun.csv",index=False)
    return result
def Refine(File):
    Laplist=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
    compile=[]
    for Lap in Laplist:
        df = File[File["Laps"] == Lap]
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day
        df["Date"] = pd.to_datetime(df["Date"]).map(lambda x: x.toordinal())
        df = df.sort_values(by="Date").reset_index(drop=True)
        for column in [col for col in df.columns if col not in ["Date","Location","Category","Laps","month","day"]and "lag" not in col.lower()]:
            print(column)
            df[column+  "_lagDate1"]= df[column].shift(1)
            df[column + "_lagDate2"] = df[column].shift(2)
            df = df.fillna(0)
        df=df.sort_values(by="Date").reset_index(drop=True)
        df.to_csv(f"Data/10KByLaps/10KMRun_Lap{Lap}.csv",index=False)
        compile.append(df)
    overall=pd.concat(compile,ignore_index=True)
    for data in overall:
        if 
    overall.to_csv("Compile10KMRun.csv", index=False)
    return File
def OverallEDA(df):
    profile = ProfileReport(df, title="Dataset Summary Report")
    profile.to_file("dataset_summary.html")

def PlotGraph(df):
    aggregated_data = df.groupby('Date')['Sales'].sum()
# rename()
dataframe=read_file()
dataframe=Refine(dataframe)
# OverallEDA(dataframe)
