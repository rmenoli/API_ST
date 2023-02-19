
import streamlit as st
import requests
import json

def get_data():
    r = requests.get("http://localhost:8000/")
    try:
        return r.json()
    except:
        print(r)


submitted = st.button("Submit")

if submitted:
    out = get_data()
    st.write(out)