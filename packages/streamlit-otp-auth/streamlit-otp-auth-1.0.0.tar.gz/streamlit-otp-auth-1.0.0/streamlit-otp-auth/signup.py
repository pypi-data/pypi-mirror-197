from dependencies import *
from generate_otp import *
from send_otp import *


if "load_state" not in st.session_state:
    st.session_state.load_state = False

def sign_up():
    st.header("Sign Up")
    name = st.text_input("Name")
    email1 = str(st.text_input("Email Address"))
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if password != confirm_password:
        st.error("Passwords do not match.")
        return
    otp = generate_otp()
    entered_otp = st.text_input("Enter OTP")
    if st.button("Send OTP") :
        send_otp_to_email(email1, otp) 
    if st.button("Sign Up"):
        st.experimental_memo.clear()
        if entered_otp == otp:
            users = {}
            try:
                with open("users.yaml", "r") as file:
                    users = yaml.load(file, Loader=yaml.FullLoader)
            except:
                pass
            if email1 in users:
                st.error("User already exists.")
            else:
                users[email1] = {"name": name, "password": password}
                with open("users.yaml", "w") as file:
                    yaml.dump(users, file)
                st.success("User signed up successfully.")

        else:
            st.error("Invalid OTP.")