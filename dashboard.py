import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="Parking Violations Dashboard", layout="wide")
st.title("🚫 Illegal Parking Violations Dashboard")

csv_path = "logs/violations.csv"

if not os.path.exists(csv_path):
    st.warning("No violations logged yet.")
else:
    df = pd.read_csv(csv_path, names=["Timestamp", "Plate", "Image"])
    search_plate = st.text_input("Search by Plate Number")
    filtered_df = df[df["Plate"].str.contains(search_plate, case=False)] if search_plate else df
    st.dataframe(filtered_df, use_container_width=True)

    for _, row in filtered_df.iterrows():
        st.image(row["Image"], caption=f"Plate: {row['Plate']} | Time: {row['Timestamp']}", width=400)