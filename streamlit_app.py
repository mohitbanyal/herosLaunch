import streamlit as st
import pandas as pd
import datetime

import streamlit as st
from streamlit_gsheets import GSheetsConnection


st.set_page_config(page_title="My Progress Log", page_icon="🛡️")


#st.write(st.secrets["connections"]["gsheets"])
conn = st.connection("gsheets",type=GSheetsConnection)

sheet_url = "https://docs.google.com/spreadsheets/d/13J8hfTd1bIXb7yY4DYmlS8rM84gCyR09-GjMFyg7qxQ"

# --- Sidebar - Data Entry (Writing to Sheet) ---
st.sidebar.header("🛡️ Log Your Progress")
with st.sidebar.form("entry_form", clear_on_submit=True):
    st.header("Log Daily Progress")
    date = st.date_input("Date", datetime.date.today())
    tech_hours = st.number_input("Tech learning (Hours)", min_value=0.0, step=0.5)
    fitness_score = st.slider("Fitness Intensity (1-10)", 1,10,5)
    weight_tracker = st.number_input("Weight meassure (Pounds)", value=200, step=1)
    notes = st.text_area("Notes (What did you learn/achive today?)")

    submit = st.form_submit_button("Save to Logs")


    if submit:
        # Load existing data, append new row, and write back (simple for small data)
        df = conn.read(
        spreadsheet=sheet_url,
        worksheet="Sheet1",
        ttl="0",
        # usecols=[0,1],
        # nrows=3,
        )

        # for row in df.itertuples():
        #     st.write(f"Mohit : Date:{row.Date}, Tech_Hours: {row.Tech_Hours}, Fitness_Intensity:{row.Fitness_Intensity}, Weight:{row.Weight}, Notes:{row.Notes}")

        new_row = pd.DataFrame([{
            "Date": date.strftime("%Y-%m-%d"),
            "Tech_Hours": tech_hours,
            "Fitness_Intensity": fitness_score,
            "Weight": weight_tracker,
            "Notes": notes,
        }])

        # Append the new row to the dataframe and write back to the sheet
        update_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=sheet_url, worksheet="Sheet1", data=update_df)

        st.sidebar.success("Training Logged Successfully!")
        st.rerun()

# Dashboard Layout
col_title, col_button = st.columns([0.9, 0.1])

with col_title:
    st.title("YeHero: The Training Room")

with col_button:
    # Add some vertical spacing (markdown hack) to align it with the title
    st.markdown("<br>", unsafe_allow_html=True) 
    # Create the button with a refresh symbol
    if st.button("🔄"):
        st.cache_data.clear()
        st.rerun() # Reruns the script, forcing a fresh load from Google Sheets

# Read data from Google Sheet with caching
df = conn.read(spreadsheet=sheet_url, worksheet="Sheet1", ttl="10m") # Cache results for 10 min

if not df.empty:
    # Ensure numerical columns are treated as numbers

    df['Tech_Hours'] = pd.to_numeric(df['Tech_Hours'])
    df['Fitness_Intensity'] = pd.to_numeric(df["Fitness_Intensity"])
    df['Weight'] = pd.to_numeric(df["Weight"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tech Hours", f"{df['Tech_Hours'].sum()}h")
    col2.metric("Avg Fitness", f"{round(df['Fitness_Intensity'].mean(), 1)}/10")
    with col3:
        last_Weight = df["Weight"].iloc[-1]
        second_last_weight = last_Weight
        if len(df) > 1:
            second_last_weight = df["Weight"].iloc[-2]
        symbol = "⬇️"
        if last_Weight - second_last_weight > 0:
            symbol = "⬆️"
        col3.metric("Latest Weight", f"{last_Weight - second_last_weight}{symbol}")
    col4.metric("Days Active", len(df))

    
    #Plot for weight
    # with col5:
    #     st.write("### 📈 Weight Average")
    #     st.line_chart(df["Weight"].ewm(span=7, adjust=False).mean())
    
    st.write("### 📈 Evolution")
    st.line_chart(df.sort_values(by="Date").set_index('Date')[['Tech_Hours', 'Fitness_Intensity',]])
    df['Date'] = pd.to_datetime(df['Date'])
    
    st.write("### 📜 Recent Logs")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No logs found. Use the sidebar to record your first hero session!")




# col1, col2 = st.columns(2)

# with col1:
#     #get data from sheet ?
#     st.metric(label="Total Tech Hours", value="12.5", delta="1.5 Today")
#     st.info("Current Focus : Python & Streamlit")
# with col2:
#     st.metric(label="Fitness Status", value="Good", delta="+1 Session")
#     st.warning("Next Goal: Consistency")