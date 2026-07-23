from ollama import chat
from langchain_community.llms import Ollama
import os
import streamlit as st
import pandas as pd
FileList = os.listdir("Data/10KByDate")
dataframelist = []
SummaryList=[]
pd.set_option('display.max_columns', None)
def plotfigure(Variable, df, filename, Fix="Laps"):
    import matplotlib.pyplot as plt
    import numpy as np
    plt.figure(figsize=(12, 6))
    data = df[[Fix, Variable]].dropna()
    if type(data[Variable][0])==str:
        data[Variable] = pd.to_datetime(data[Variable], format="%d%b%Y")
        data[Variable] = data[Variable].dt.strftime("%Y%m%d").astype(int)
    # print(data[Variable][0],type(data[Variable][0]))
    # Original line
    plt.plot(
        data[Fix],
        data[Variable],
        marker='o',
        label=Variable
    )

    # Linear regression trendline
    x = data[Fix].values
    y = data[Variable].values

    # Only fit if enough points exist
    if len(x) > 1:
        slope, intercept = np.polyfit(x, y, 1)
        trendline = slope * x + intercept

        plt.plot(
            x,
            trendline,
            linestyle='--',
            label=f'Trendline (slope={slope:.3f})'
        )

    plt.xlabel(Fix)
    plt.ylabel(Variable)
    plt.title(f'{Variable} by {Fix}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"Plotgraph/{filename}_{Variable}.png", dpi=200)
    plt.close()

def tohms(total_seconds):
    # Ensure total_seconds is treated as an integer
    total_seconds = int(total_seconds)

    hours = total_seconds // 3600  # No comma!
    minutes = (total_seconds % 3600) // 60  # No comma!
    seconds = total_seconds % 60
    minutes=minutes+(hours*60)
    time=float(f"{minutes}.{seconds}")
    # print(time)
    # Use an f-string to format as HH:MM:SS
    # ':02d' ensures single digits get a leading zero (e.g., '05' instead of '5')
    return time
for count,file in enumerate(FileList):
    Date, Location, Category = file.split(".")[0].split("_")
    df = pd.read_csv(f"10KByDate/" + file)
    df["Date"]=Date
    df["Location"]=Location
    for column in df.columns:
        if "Pace" in column or "Time" in column:
            df[column]=df[column].apply(tohms)
        if column not in ["Date","Location","Condition_Category"]:
            df[column] = df[column].round(2)
        if column not in ("Laps","Location","Date") and count==len(FileList):
            plotfigure(column, df,file, "Laps")
    # print(df.describe())
    dataframelist.append(df)
    # SummaryList.append({"Date":Date,"Location":Location,"Summary":df.describe()})


result = pd.concat(dataframelist, ignore_index=True)
print(result)
prediction = pd.read_csv(f"Prediction/" + "Prediction_2026-06-29")

llm = Ollama(model="llama3")
st.title("🏃‍♂️ Personal Running Coach Chatbot")
st.write("Ask me to generate reports or give training suggestions based on your data!")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
reportmessage='''Give me:
                1) Performance analysis
                2)Training recommendation
'''

st.session_state.messages.append({"role": "user", "content": reportmessage})
with st.chat_message(reportmessage):
    st.markdown(reportmessage)

    # Construct the prompt with context
system_prompt = f"You are an expert running coach. Here is the user's running data:\n\n{result}\n\n"
full_query = system_prompt + f"User question: {reportmessage}"

    # Generate response
with st.chat_message("assistant"):
    response_placeholder = st.empty()
# Call the local LLM
    response = llm.invoke(full_query)
    response_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# prompt = f"""
# You are a professional running coach.
#
# Analyze this runner:
# {result}
# Analyze the prediction:
# {prediction}
# Provide:
# 1. Overall Summary of the run (Central tendency, Max value, Min Value) in a table form
# 2. Evaluate the prediction
# 3. Performance analysis
# # 4. Trends
# # 5. Strengths
# # 6. Weaknesses
# # 7. Injury risks
# # 8. 10K improvement suggestions
# # 9. Training recommendation
# """
# print("analyhsing")
# response = chat(
#     model="qwen3:8b",
#     messages=[
#         {"role":"user","content":prompt}
#     ]
# )
#
# report = response.message.content
# print(report)
