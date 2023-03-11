import streamlit as st
import requests
import json
import streamlit_authenticator as stauth

def get_all_the_values():
    r = requests.get("http://127.0.0.1:8000/listEmbeddedElements")
    try:
        return r.json()
    except:
        print(r)

def search(term_to_search):
    r = requests.get(f"http://127.0.0.1:8000/getClosestEntity/{term_to_search}%20?n_closes_element=1")
    try:
        return r.json()
    except:
        print(r)

def authenticate(usr, psw):
    data = {
        'username': usr,
        'password':psw
    }
    r = requests.post('http://127.0.0.1:8000/token', data=data)
    try:
        return r.json()
    except:
        print(r)


with st.form("see_all_val_in_string"):
    st.write("See all the values in the index")
    submitted_all_values = st.form_submit_button("Submit")

    if submitted_all_values:
        out = get_all_the_values()
        st.write(out)


with st.form("search_index"):
    st.write("Search")
    term_to_search = st.text_input("", 'Term to search')
    submitted = st.form_submit_button("Submit")
    if submitted:
        out = search(term_to_search)
        st.write(out)

access_token = ""
with st.form("authenticate"):
    st.write("Authentication")
    user = st.text_input("", 'username')
    psw = st.text_input("", 'psw')
    submitted = st.form_submit_button("Submit")
    if submitted:
        out = authenticate(user,psw)
        if 'access_token' in out.keys():
            access_token = out['access_token']
            st.write('authenticated')
        else:
            st.write(out)
