import streamlit as st
import pandas as pd

st.title("phonebook clearner")

upload_filre = st.file_uploader("upload your phonebook(.csv or xlsx)". type=["csv","xlsv"]

if uploaded_file:


    if uploaded_file.name.endswith('.csv):

       df = pd.read_csv(uploaded
    else:
       df = pd.read_excel(uploaded_file)


     st.subheader('Raw Data')
     st.write(df.head())


     df.columns = [col.strip() for col in df.columns] 


     if 'Name' in df.columns and 'Phone' in df.columns:
         df['Name'] = df['Name'].astype(str).str.strip()
         df['Phone'] = df['Phone'].astype(str).str.replace(r'\D','',regex=True)



    st.subheader("Cleaned Data")
    st.write(df.head())

    csv= df.to_csv(index=false)
    st.download_csv("Download Cleaned csv", csv, "cleaned_phonebbook.csv","text/csv") 



