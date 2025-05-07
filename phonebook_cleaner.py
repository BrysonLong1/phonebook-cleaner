import streamlit as st
import pandas as pd

st.title("📇 Phonebook Cleaner")

uploaded_file = st.file_uploader("Upload your phonebook (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    # Load file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader('Raw Data')
    st.write(df.head())

    # Clean column headers
    df.columns = [col.strip() for col in df.columns]

    # Let user select columns
    name_col = st.selectbox("Select the column for names:", df.columns)
    phone_col = st.selectbox("Select the column for phone numbers:", df.columns)

    # Clean data
    df[name_col] = df[name_col].astype(str).str.strip()
    df[phone_col] = df[phone_col].astype(str).str.replace(r'\D', '', regex=True)

    # Extract area codes

    df[phone_col] = df[phone_col].str.lstrip('1')
    df['Area Code'] = df[phone_col].str[:3]

    # Group by area code
    area_code_group = df.groupby('Area Code').size().reset_index(name='Count')

    st.subheader("Cleaned Data")
    st.write(df[[name_col, phone_col, 'Area Code']].head())

    st.subheader("📊 Area Code Breakdown")
    st.write(area_code_group)
    st.bar_chart(area_code_group.set_index('Area Code'))

    # Download cleaned file
    csv = df[[name_col, phone_col, 'Area Code']].to_csv(index=False)
    st.download_button("📥 Download Cleaned CSV", csv, "cleaned_phonebook.csv", "text/csv")

   

    

