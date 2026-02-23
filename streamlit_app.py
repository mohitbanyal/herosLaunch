import streamlit as st
import streamlit_authenticator as sa
import os
from dotenv import load_dotenv
from streamlit_gsheets import GSheetsConnection
from dashboard_page import show_dashboard
from load_connections import _conn , load_data

import uuid

# Load the environment variables from the .env file
load_dotenv()

st.set_page_config(page_title="YeHero Training Log", page_icon="🛡️", layout="wide")

#create a connection
#conn = st.connection("gsheets",type=GSheetsConnection)
#sheet_url = os.getenv("GOOGLE_SHEET_URL")
# df = conn.read(
#     spreadsheet=sheet_url,
#     worksheet="main",
# )

con = _conn()
df = load_data(con,"main")


usernames = df['Usernames']
names = df['Names']
passwords = df['Passwords']

#hashed_passwords = [sa.Hasher.hash(pwd) for pwd in passwords]

config = {
    "cookie" :{
        'expiry_days':30,
        'key': str(uuid.uuid4()),
        'name':'yehero_cookie'
    },
    'credentials':{'usernames':{}}
}

#populate config 
for i, user in enumerate(usernames):
    config['credentials']['usernames'][user] = {
        'email': f'{user}@yehero.com',
        'name': names[i],
        'password':passwords[i]
    }

authenticator = sa.Authenticate(
    config['credentials'],
    config['cookie']['expiry_days'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login("main")

authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status == True:
    show_dashboard(name,username)