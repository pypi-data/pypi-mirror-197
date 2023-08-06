from dependencies import *
from generate_otp import *
from send_otp import *
from reset_password import *

if "load_state" not in st.session_state:
    st.session_state.load_state = False

def log_in():
    st.header("Log In")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        users = {}
        try:
            with open("users.yaml", "r") as file:
                users = yaml.load(file, Loader=yaml.FullLoader)
        except:
            pass
        if email not in users:
            st.error("User does not exist.")
        elif users[email]["password"] != password:
            st.error("Invalid password.")
        else:
            st.success("Logged in successfully.")
    else:
        reset_password()
