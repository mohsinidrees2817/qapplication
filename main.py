import streamlit as st
from login import authenticate, getuser, update_password
from chatapplication import user_details_page

if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'auth_response' not in st.session_state:
    st.session_state['auth_response'] = None

if 'isuserloggedin' not in st.session_state:
    st.session_state['isuserloggedin'] = False


if 'username' not in st.session_state:
    st.session_state['username'] = None

if 'usercredentials' not in st.session_state:
    st.session_state.usercredentials = None

def main_page():
    if st.session_state.user != None:
        user_details_page()
    else:
        global user_data
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            auth_response = authenticate(username, password)
            if auth_response:
                user_data = auth_response
                if 'ChallengeName' in auth_response and auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
                    # st.warning("New password is required. Please reset your password.")
                    update_password(username, password, auth_response['Session'])
                else:
                    st.success("Authentication successful!")
                    st.success("Waiting for Other Services Access verification")
                    st.session_state['auth_response'] = auth_response
                    st.session_state['isuserloggedin'] = True
                    id_token = auth_response['AuthenticationResult']['IdToken']
                    access_token = auth_response['AuthenticationResult']['AccessToken']
                    getuser(id_token, access_token)
    


       

if 'runpage' not in st.session_state:
    st.session_state.runpage = main_page

st.session_state.runpage()
