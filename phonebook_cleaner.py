import streamlit as st
import pandas as pd

st.title("📇 Phonebook Cleaner")

uploaded_file = st.file_uploader("Upload your phonebook (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    # Load the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader('Raw Data')
    st.write(df.head())

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Clean name and phone columns
    if 'Name' in df.columns and 'Phone' in df.columns:
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Phone'] = df['Phone'].astype(str).str.replace(r'\D', '', regex=True)

        # Extract area code
        df['Area Code'] = df['Phone'].str[:3]

        # Group by area code
        area_code_group = df.groupby('Area Code').size().reset_index(name='Count')

        st.subheader("Cleaned Data")
        st.write(df.head())

        # Show area code breakdown
        st.subheader("📊 Area Code Breakdown")
        st.write(area_code_group)

        # Optional: Bar chart of area codes
        st.bar_chart(area_code_group.set_index('Area Code'))

        # Allow download
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Cleaned CSV", csv, "cleaned_phonebook.csv", "text/csv")
    else:
        st.error("The file must contain 'Name' and 'Phone' columns.")

   

    

