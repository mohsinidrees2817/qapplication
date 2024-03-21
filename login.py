import streamlit as st
import boto3


USER_POOL_ID = st.secrets["USER_POOL_ID"]
CLIENT_ID = st.secrets["CLIENT_ID"]
REGION = st.secrets["REGION"]
IDENTITYPOOLID = st.secrets["IDENTITY_POOL_ID"]
ACCOUNTID = st.secrets["ACCOUNT_ID"]


def authenticate(username, password):
    try:
        client = boto3.client('cognito-idp', region_name=REGION)
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        st.session_state['auth_response'] = response
        return response
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return None


def getuser(idtoken, access_token):
    try:
        clientidp = boto3.client('cognito-idp', region_name=REGION)

        client = boto3.client('cognito-identity', region_name=REGION)
        user = clientidp.get_user(
                 AccessToken=access_token
        )   
        username = user["Username"]
        logins = {
            f'cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}': idtoken
        }
        response = client.get_id(
            AccountId=ACCOUNTID,
            IdentityPoolId=IDENTITYPOOLID,	
            Logins=logins
        )
        identityId = response['IdentityId']
        
        responsee = client.get_credentials_for_identity(
                IdentityId=identityId,
                Logins=logins
        )
        accesskeyID = responsee['Credentials']['AccessKeyId']
        secretkey = responsee['Credentials']['SecretKey']
        sessiontoken = responsee['Credentials']['SessionToken']


        sts_client = boto3.client('sts',
        aws_access_key_id=accesskeyID,
        aws_secret_access_key=secretkey,
        aws_session_token=sessiontoken)

        responseforUserid = sts_client.get_caller_identity()
        userid = responseforUserid["UserId"]
        arn  = responseforUserid["Arn"]
        userdata = {
            "accesskeyID": accesskeyID,
            "secretkey": secretkey,
            "sessiontoken": sessiontoken,
            "userid": userid,
            "arn": arn,
            "username": username
        }
        st.session_state['user'] = userdata
        # st.session_state.runpage = user_details_page
        st.experimental_rerun()

    except Exception as e:
        st.error("Failed to get credentials: " + str(e))

    





def get_open_id_token(identity_id, user_id_token):
    client = boto3.client('cognito-identity', region_name=REGION)
    
    logins = {
        f'cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}': user_id_token
    }
    
    try:
        response = client.get_open_id_token(
            IdentityId=identity_id,
            Logins=logins
        )
        # return response
        st.write(response)

    except Exception as e:
        st.error("Failed to get credentials: " + str(e))



def respond_to_auth_challenge(username, new_password, session):
    try:
        client = boto3.client('cognito-idp', region_name=REGION)
        response = client.respond_to_auth_challenge(
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ClientId=CLIENT_ID,
            ChallengeResponses={
                'USERNAME': username,
                'NEW_PASSWORD': new_password
            },
            Session=session
        )
        return response
    except Exception as e:
        st.error(f"Error updating password: {e}")
        return None






def update_password(username,password, session):
    st.header("Updating password")
    st.write("As it is by default forced to update for self created users")
    new_password = password
    update_response = respond_to_auth_challenge(username, new_password, session)
    if update_response:
        st.success("Password updated successfully!")
    else:
        st.error("Error updating password. Please try again.")



