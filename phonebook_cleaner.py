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

    # Let user choose columns
    name_col = st.selectbox("Select the column for names:", df.columns)
    phone_col = st.selectbox("Select the column for phone numbers:", df.columns)

    # Clean values
    df[name_col] = df[name_col].astype(str).str.strip()
    df[phone_col] = df[phone_col].astype(str).str.replace(r'\D', '', regex=True)

    # Remove leading '1' if it's an 11-digit US number
    df[phone_col] = df[phone_col].apply(lambda x: x[1:] if len(x) == 11 and x.startswith('1') else x)

    # Extract area code
    df['Area Code'] = df[phone_col].str[:4]

    # Group by area code
    area_code_group = df.groupby('Area Code').size().reset_index(name='Count')

    # Display cleaned data safely
    if name_col in df.columns and phone_col in df.columns and 'Area Code' in df.columns:
        st.subheader("Cleaned Data")
        st.write(df[[name_col, phone_col, 'Area Code']].head())
    else:
        st.error("One or more selected columns do not exist in the data.")

    # Show area code summary
    st.subheader("📊 Area Code Breakdown")
    st.write(area_code_group)
    st.bar_chart(area_code_group.set_index('Area Code'))

    # Download cleaned CSV
    csv = df[[name_col, phone_col, 'Area Code']].to_csv(index=False)
    st.download_button("📥 Download Cleaned CSV", csv, "cleaned_phonebook.csv", "text/csv")

    

   

    

