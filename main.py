import streamlit as st
from login import login
from chatapplication import user_details_page
from streamlit_option_menu import option_menu


if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'auth_response' not in st.session_state:
    st.session_state['auth_response'] = None

if 'isuserloggedin' not in st.session_state:
    st.session_state['isuserloggedin'] = False


if 'username' not in st.session_state:
    st.session_state['username'] = None



# if st.session_state['user'] is not None:
#     selected = option_menu (
#         menu_title=None,
#         options=["Home", "Projects", "Contact"],
#         icons=["house", "book", "envelope"], 
#         menu_icon="cast", 
#         default_index=0,
#         orientation="horizontal",
#     )
#     if selected =="Home":
#         st.title(f"You have selected {selected}")
#     if selected == "Projects":
#         st.title(f"You have selected {selected}")
#     if selected == "Contact":
#         st.title(f"You have selected {selected}")




# st.set_page_config(page_title="Chat Application", page_icon=":speech_balloon:")

if 'usercredentials' not in st.session_state:
    st.session_state.usercredentials = None

def main_page():
    #if user loged in show user details page esle login
    if st.session_state['isuserloggedin']:
        user_details_page()
    else:
        login()
    # st.session_state.runpage = login
    # st.session_state.runpage = login
    # st.session_state.runpage()
    # st.experimental_rerun()

       

if 'runpage' not in st.session_state:
    st.session_state.runpage = main_page

st.session_state.runpage()
