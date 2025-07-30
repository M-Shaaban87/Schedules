import pandas as pd
import streamlit as st
import io
import base64

# Embedded Excel content (base64 encoded)
embedded_excel = """UEsDBBQABgAIAAAAIQCvh2ASgwEAAGMFAAATAAgCW0NvbnRlbnRfVHlwZXNdLnhtbCCiBAIooAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""

# Decode and load the Excel file
excel_bytes = base64.b64decode(embedded_excel)
xls = pd.ExcelFile(io.BytesIO(excel_bytes))
df = xls.parse("Staff", header=None)

# Extract the name column and the data
names = df.iloc[2:, 0].dropna().unique()

# Extract years and semesters from first two rows
year_row = df.iloc[0, 1:]
semester_row = df.iloc[1, 1:]
columns = list(zip(year_row, semester_row))

# Build a structured mapping: year -> semester -> column index
data_map = {}
for idx, (year, semester) in enumerate(columns):
    if pd.isna(year) or pd.isna(semester):
        continue
    if year not in data_map:
        data_map[year] = {}
    data_map[year][semester] = idx + 1  # +1 to match df columns

st.title("Academic Hours Distribution")

# Select name
selected_name = st.selectbox("Select Staff Name", list(names))

# Select year
selected_year = st.selectbox("Select Academic Year", list(data_map.keys()))

# Filter semesters for selected year
semesters = list(data_map[selected_year].keys()) if selected_year in data_map else []
selected_semester = st.selectbox("Select Semester", semesters)

# Show result
if st.button("Get Academic Hours"):
    if selected_name and selected_year and selected_semester:
        col_idx = data_map.get(selected_year, {}).get(selected_semester)
        row = df[df.iloc[:, 0] == selected_name]
        value = row.iloc[0, col_idx] if not row.empty else "N/A"
        st.success(f"Academic Hours for {selected_name} in {selected_year} - {selected_semester}: {value}")
    else:
        st.warning("Please select all options.")
