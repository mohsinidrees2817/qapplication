import streamlit as st
import boto3


APPLICATIONID = st.secrets["APPLICATION_ID"]
USERGROUP = st.secrets["USER_GROUP"]

conversationID = None
parentMessageID = None

if 'messages' not in st.session_state:
    st.session_state.messages = []




def new_chat_with_Q(prompt):
    global conversationID
    global parentMessageID
    try:
        client = boto3.client('qbusiness', region_name="us-west-2",
                aws_access_key_id=st.session_state['user']['accesskeyID'],
                aws_secret_access_key=st.session_state['user']['secretkey'],
                aws_session_token=st.session_state['user']['sessiontoken']
                )
        response = client.chat_sync(
                applicationId=APPLICATIONID,
                userGroups=[
                    USERGROUP,
                ],
                userId=st.session_state['user']['userid'],
                userMessage=prompt
        )
        parentMessageID = response["systemMessageId"]
        conversationID = response["conversationId"]
        return response["systemMessage"]
    except Exception as e:
        st.error("Failed to chat with api: " + str(e))

def continue_chat_with_Q(prompt):
    global conversationID
    global parentMessageID
    try:
        client = boto3.client('qbusiness', region_name="us-west-2",
                aws_access_key_id=st.session_state['user']['accesskeyID'],
                aws_secret_access_key=st.session_state['user']['secretkey'],
                aws_session_token=st.session_state['user']['sessiontoken']
                )
        response = client.chat_sync(
                applicationId=APPLICATIONID,
                userGroups=[
                    USERGROUP,
                ],
                userId=st.session_state['user']['userid'],
                userMessage=prompt,
                conversationId=conversationID,
                parentMessageId=parentMessageID,
        )

        parentMessageID = response["systemMessageId"]
        return response["systemMessage"]
    except Exception as e:
        st.error("Failed to chat with api: " + str(e))  

        

def list_conversations():
    try:
        client = boto3.client('qbusiness', region_name="us-west-2",
                    aws_access_key_id=st.session_state['user']['accesskeyID'],
                    aws_secret_access_key=st.session_state['user']['secretkey'],
                    aws_session_token=st.session_state['user']['sessiontoken']
                    )
        response = client.list_conversations(
        applicationId=APPLICATIONID,
        maxResults=50,
        userId=st.session_state['user']['userid']
        )
        return response["conversations"]
    except Exception as e:
        st.error("Failed to chat with api: " + str(e))

def get_messages():
    global parentMessageID
    st.session_state.messages = []
    client = boto3.client('qbusiness', region_name="us-west-2",
                    aws_access_key_id=st.session_state['user']['accesskeyID'],
                    aws_secret_access_key=st.session_state['user']['secretkey'],
                    aws_session_token=st.session_state['user']['sessiontoken']
                    )
    response = client.list_messages(
        applicationId=APPLICATIONID,
        conversationId=conversationID,
        maxResults=100,
        userId=st.session_state['user']['userid']
    )
    previous_messages = response["messages"]
    previous_messages= previous_messages[::-1]
    for message in previous_messages:
        role = message["type"]
        content = message["body"]
        if role == "USER":
            st.session_state.messages.append({"role": "user", "content": content})
        elif role == "SYSTEM":
            st.session_state.messages.append({"role": "system", "content": content})
        
    parentMessageID = response["messages"][0]["messageId"]


def start_new_chat():
    # Implement the functionality to start a new chat here
    global conversationID
    global parentMessageID
    conversationID = None
    parentMessageID = None
    st.session_state.messages = []



def user_details_page():
    global conversationID
    global parentMessageID
    st.markdown(
    """
        <style>
        button {
            height: auto;
            padding-top: 10px !important;
            padding-bottom: 10px !important;            
        }
        </style>
    """,
    unsafe_allow_html=True,
    )
    username = st.session_state['user']['username']
    st.sidebar.write("User Name:", username)
    st.sidebar.title("User chat History")
    if st.sidebar.button("Start New Chat............"):
        start_new_chat()
    
    conversations = list_conversations()
    for conv in conversations:
        title = conv["title"]
        conversationId = conv["conversationId"]
        if st.sidebar.button(title, key=conversationId):
            conversationID = conversationId
            get_messages()
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    


    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # React to user input
    prompt = st.chat_input("what is Hybrid Connectivity?")

    # if st.button("Send"):
    if prompt:
        # Get assistant response
        if conversationID and parentMessageID:
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            system_response = continue_chat_with_Q(prompt)
            # Display assistant response
            with st.chat_message("system"):
                st.markdown(system_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "system", "content": system_response})
            
        else:
            st.session_state.messages = []
            with st.chat_message("user"):
                st.markdown(prompt)
        # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt}) 
            system_response = new_chat_with_Q(prompt)
            # Display assistant response
            with st.chat_message("system"):
                st.markdown(system_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "system", "content": system_response})

    if not st.session_state.messages and not conversationID and not parentMessageID:
        # Display the questions
        st.title("Start New Chat")
        st.write("1. Explain two main categories.")
        st.write("2. What is the main difference between the two categories?")
        st.write("3. What is Hybrid Design?")
        st.write("4. what is Hybrid Connectivity?") 
        


